#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.keycode.functionality
:brief: Hid Keyboard keycode functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/22
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
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.keycode.keycode import KeyCodeTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyCodeFunctionalityTestCase(KeyCodeTestCase):
    """
    Validate Keyboard KeyCode functionality TestCases
    """

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SingleKeystroke')
    def test_all_available_keys(self):
        """
        Check if all keys are working properly
        """
        self._test_key_code()

        self.testCaseChecked("FUN_MEMB_0001")
    # end def test_all_available_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_all_key_pairs(self):
        """
        Check if all keys could be used to create a combination of 2 keys pressed simultaneously.
        """
        self.kosmos.sequencer.offline_mode = True
        pair_of_keys_list = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=2, random=False)

        for key_pair in pair_of_keys_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate pressing the key pair {str(key_pair[0])} & {str(key_pair[1])}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_pair,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate releasing the key pair {str(key_pair[0])!s} & {str(key_pair[1])!s}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_pair,
                                                               delay=ButtonStimuliInterface.DEFAULT_DURATION)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_pair in pair_of_keys_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the key pair '
                                      f'{str(key_pair[0])!s} & {str(key_pair[1])!s}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_pair)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_pair[index], MAKE))
            # end for
            for index in range(len(key_pair)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_pair[index], BREAK))
            # end for
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0002")
    # end def test_all_key_pairs

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_all_key_triplets(self):
        """
        Check if all keys could be used to create a combination of 3 keys pressed simultaneously.
        """
        self.kosmos.sequencer.offline_mode = True
        key_triplets = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=3, random=False)

        for key_triplet in key_triplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate pressing the key triplet {str(key_triplet[0])!s} & '
                                     f'{str(key_triplet[1])!s} & {str(key_triplet[2])!s}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_triplet,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate releasing the key triplet {str(key_triplet[0])!s} & '
                                     f'{str(key_triplet[1])!s} & {str(key_triplet[2])!s}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_triplet,
                                                               delay=ButtonStimuliInterface.DEFAULT_DURATION)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_triplet in key_triplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID Keyboard report for the key triplet '
                                      f'{key_triplet[0]!s} & {key_triplet[1]!s} & {key_triplet[2]!s}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_triplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_triplet[index], MAKE))
            # end for
            for index in range(len(key_triplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_triplet[index], BREAK))
            # end for
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0003")
    # end def test_all_key_triplets

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    def test_all_key_quadruplets(self):
        """
        Check if all keys could be used to create a combination of 4 keys pressed simultaneously.
        """
        self.kosmos.sequencer.offline_mode = True
        key_quadruplets = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=4, random=False)

        for key_quadruplet in key_quadruplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key presses on the quadruplet '
                                     f'{str(key_quadruplet[0])!s} & {str(key_quadruplet[1])!s} & '
                                     f'{str(key_quadruplet[2])!s} & {str(key_quadruplet[3])!s}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_quadruplet,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key releases on the quadruplet '
                                     f'{str(key_quadruplet[0])!s} & {str(key_quadruplet[1])!s} & '
                                     f'{str(key_quadruplet[2])!s} & {str(key_quadruplet[3])!s}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_quadruplet,
                                                               delay=ButtonStimuliInterface.DEFAULT_DURATION)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_quadruplet in key_quadruplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the key quadruplet '
                                      f'{str(key_quadruplet[0])!s} & {str(key_quadruplet[1])!s} &'
                                      f'{str(key_quadruplet[2])!s} & {str(key_quadruplet[3])!s}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_quadruplet[index], MAKE))
            # end for
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(key_quadruplet[index], BREAK))
            # end for
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0004")
    # end def test_all_key_quadruplets

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT,))
    def test_all_keys_with_left_shift(self):
        """
        Check all keys are working properly if preceded by a left shift key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0005")
    # end def test_all_keys_with_left_shift

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_all_keys_with_right_shift(self):
        """
        Check all keys are working properly if preceded by a right shift key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Emulate a keystroke on all supported keys when the right shift key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_SHIFT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0006")
    # end def test_all_keys_with_right_shift

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL,))
    def test_all_keys_with_left_ctrl(self):
        """
        Check all keys are working properly if preceded by a left control key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Emulate a keystroke on all supported keys when the left control key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0007")
    # end def test_all_keys_with_left_ctrl

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_all_keys_with_right_ctrl(self):
        """
        Check all keys are working properly if preceded by a right control key press.
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, 'Emulate a keystroke on all supported keys when the right control key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[right_ctrl_key_id])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0008")
    # end def test_all_keys_with_right_ctrl

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_all_keys_with_left_alt(self):
        """
        Check all keys are working properly if preceded by a left alt key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left alt key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0009")
    # end def test_all_keys_with_left_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_all_keys_with_right_alt(self):
        """
        Check all keys are working properly if preceded by a right alt key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right alt key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0010")
    # end def test_all_keys_with_right_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    def test_all_keys_with_left_win(self):
        """
        Check all keys are working properly if preceded by a left win key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left win key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0011")
    # end def test_all_keys_with_left_win

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_all_keys_with_right_win(self):
        """
        Check all keys are working properly if preceded by a right win key press.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right win key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0012")
    # end def test_all_keys_with_right_win

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL,))
    def test_all_keys_with_left_shift_left_ctrl(self):
        """
        Check all keys are working properly if preceded by a left shift & a left control key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the left control '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT,
                                                                            KEY_ID.KEYBOARD_LEFT_CONTROL])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0013")
    # end def test_all_keys_with_left_shift_left_ctrl

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    def test_all_keys_with_left_shift_left_win(self):
        """
        Check all keys are working properly if preceded by a left shift & a left win key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the left win keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT,
                                                                            KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0014")
    # end def test_all_keys_with_left_shift_left_win

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_all_keys_with_left_shift_left_alt(self):
        """
        Check all keys are working properly if preceded by a left shift & a left alt key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the left alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT,
                                                                            KEY_ID.KEYBOARD_LEFT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0015")
    # end def test_all_keys_with_left_shift_left_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_all_keys_with_left_shift_right_ctrl(self):
        """
        Check all keys are working properly if preceded by a left shift & a right control key presses.
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift '
                                 'and the right control keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT,
                                                                            right_ctrl_key_id])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0016")
    # end def test_all_keys_with_left_shift_right_ctrl

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_all_keys_with_left_shift_right_win(self):
        """
        Check all keys are working properly if preceded by a left shift & a right win key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the right win keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT,
                                                                            KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0017")
    # end def test_all_keys_with_left_shift_right_win

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_all_keys_with_left_shift_right_alt(self):
        """
        Check all keys are working properly if preceded by a left shift & a right alt key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift '
                                 'and the right alt keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT,
                                                                            KEY_ID.KEYBOARD_RIGHT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0018")
    # end def test_all_keys_with_left_shift_right_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    def test_all_keys_with_left_ctrl_left_win(self):
        """
        Check all keys are working properly if preceded by a left control & a left win key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control and the left win '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL,
                                                                            KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0019")
    # end def test_all_keys_with_left_ctrl_left_win

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_all_keys_with_left_ctrl_left_alt(self):
        """
        Check all keys are working properly if preceded by a left control & a left alt key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control and the left alt '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL,
                                                                            KEY_ID.KEYBOARD_LEFT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0020")
    # end def test_all_keys_with_left_ctrl_left_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_all_keys_with_left_ctrl_right_shift(self):
        """
        Check all keys are working properly if preceded by a left control & a right shift key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control and the right shift '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL,
                                                                            KEY_ID.KEYBOARD_RIGHT_SHIFT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0021")
    # end def test_all_keys_with_left_ctrl_right_ctrl

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_all_keys_with_left_ctrl_right_win(self):
        """
        Check all keys are working properly if preceded by a left control & a right win key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control and the right win '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL,
                                                                            KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0022")
    # end def test_all_keys_with_left_ctrl_right_win

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_all_keys_with_left_ctrl_right_alt(self):
        """
        Check all keys are working properly if preceded by a left control & a right alt key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control and the right alt '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL,
                                                                            KEY_ID.KEYBOARD_RIGHT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0023")
    # end def test_all_keys_with_left_ctrl_right_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_all_keys_with_left_win_left_alt(self):
        """
        Check all keys are working properly if preceded by a left win & a left alt key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left win and the left alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,
                                                                            KEY_ID.KEYBOARD_LEFT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0024")
    # end def test_all_keys_with_left_win_left_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_all_keys_with_left_win_right_alt(self):
        """
        Check all keys are working properly if preceded by a left win & a right alt key presses.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left win and the right alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,
                                                                            KEY_ID.KEYBOARD_RIGHT_ALT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0025")
    # end def test_all_keys_with_left_win_right_alt

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_not_fn_keys_with_fn_key(self):
        """
        Press on Fn-Key then check if keys that are not F-Keys returned the right key code.
        """
        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self, excluded_keys=[])

        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)

        for (key_id,) in keys:
            if key_id in fn_keys.values():
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for (key_id,) in keys:
            if key_id in fn_keys.values():
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report on key id {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0026")
    # end def test_not_fn_keys_with_fn_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('SimultaneousKeystrokes')
    def test_mac_os_all_keys(self):
        """
        Check all FW key codes are correct when an macOS has been detected.
        """
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in macOS mode: long press on fn + o')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in mac os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0027")
    # end def test_mac_os_all_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('KeyMatrix')
    def test_mac_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when a macOS has been detected.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in macOS mode: long press on fn + o')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key press on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                         delay=ButtonStimuliInterface.DEFAULT_DURATION)
        assert self.button_stimuli_emulator.fn_pressed, 'FN key has not been correctly pressed !'

        for key_id in fn_keys.values():
            if KEY_ID.FN_LOCK in fn_keys and key_id == fn_keys[KEY_ID.FN_LOCK]:
                # Skip Fn-lock key in this test
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key release on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(5)

        for key_id in iter(fn_keys.keys()):
            if key_id == KEY_ID.FN_LOCK:
                # Fn-lock key has been skipped in this test
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in mac os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0028")
    # end def test_mac_os_fn_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.FN_KEY, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_os_not_fn_keys_with_fn_key(self):
        """
        Press on Fn-Key then check if keys that are not F-Keys returned the right key code
        when a macOS has been detected.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in macOS mode: long press on fn + o')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION, delay=1)

        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self, excluded_keys=[])

        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)

        for (key_id,) in keys:
            if key_id in fn_keys.values():
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for (key_id,) in keys:
            if key_id in fn_keys.values():
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID Keyboard report for each keys')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0029")
    # end def test_mac_os_not_fn_keys_with_fn_key

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    @services('SimultaneousKeystrokes')
    def test_ipad_os_all_keys(self):
        """
        Check all FW key codes are correct when an iPadOS has been detected.
        """
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in iPadOS mode: long press on fn + i')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.IPAD, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=1)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in ipad os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.IPAD)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.IPAD)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0030")
    # end def test_ipad_os_all_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    @services('KeyMatrix')
    def test_ipad_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when an iPadOS has been detected.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in iPadOS mode: long press on fn + i')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.IPAD, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key press on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                         delay=ButtonStimuliInterface.DEFAULT_DURATION)
        assert self.button_stimuli_emulator.fn_pressed, 'FN key has not been correctly pressed !'

        for key_id in fn_keys.values():
            if KEY_ID.FN_LOCK in fn_keys and key_id == fn_keys[KEY_ID.FN_LOCK]:
                # Skip Fn-lock key in this test
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key release on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(5)

        for key_id in iter(fn_keys.keys()):
            if key_id == KEY_ID.FN_LOCK:
                # Fn-lock key has been skipped in this test
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in ipad os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.IPAD)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.IPAD)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0031")
    # end def test_ipad_os_fn_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_NO_US_1, KEY_ID.KEYBOARD_NO_US_45,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_inverted_mac_os_keys(self):
        """
        Check the keyboard shortcut Fn+U (long press) that will activate the option of having standard HID codes 0x35
        and 0x64 for these two keys.
        It will work as a toggle, by default these two HID key codes are inverted,
        then after Fn+U they won't be inverted.
        Again if Fn+U is pressed, two keys get again inverted.

        cf OS Selection User Experience 1.2.6:
        https://docs.google.com/document/d/1v0dRllFLLaG0icASJuB_266Gqoch8SnHCwxDUTWw1L4/edit#
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in inverted macOS mode: long press on fn + u')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.INVERTED_MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in [(KEY_ID.KEYBOARD_NO_US_1,), (KEY_ID.KEYBOARD_NO_US_45,), ]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        # Switch back to regular macOS mode: long press on fn + u
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.INVERTED_MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for (key_id,) in [(KEY_ID.KEYBOARD_NO_US_1,), (KEY_ID.KEYBOARD_NO_US_45,), ]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in inverted mac os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.INVERTED_MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.INVERTED_MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0032")
    # end def test_inverted_mac_os_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_C,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.CHROME_OS,))
    @services('SimultaneousKeystrokes')
    @bugtracker("ChromeOS_Backlight_KeyCode")
    def test_chrome_os_all_keys(self):
        """
        Check all FW key codes are correct when a Chrome OS has been detected.

        JIRA: https://jira.logitech.io/browse/NRF52-468
        """
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in Chrome OS mode: long press on fn + c')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.CHROME, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos Board
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in Chrome OS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.CHROME)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.CHROME)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0040")
    # end def test_chrome_os_all_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_C,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.CHROME_OS,))
    @services('KeyMatrix')
    def test_chrome_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when a Chrome OS has been detected.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in Chrome OS mode: long press on fn + c')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.CHROME, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key press on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                         delay=ButtonStimuliInterface.DEFAULT_DURATION)
        assert self.button_stimuli_emulator.fn_pressed, 'FN key has not been correctly pressed !'

        for key_id in fn_keys.values():
            if KEY_ID.FN_LOCK in fn_keys and key_id == fn_keys[KEY_ID.FN_LOCK]:
                # Skip Fn-lock key in this test
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key release on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos Board
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(5)

        for key_id in iter(fn_keys.keys()):
            if key_id == KEY_ID.FN_LOCK:
                # Fn-lock key has been skipped in this test
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in Chrome OS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.CHROME)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.CHROME)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0041")
    # end def test_chrome_os_fn_keys

    @features('Keyboard')
    @features('KeyCode')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.FN_KEY, KEY_ID.KEYBOARD_C, ))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.CHROME_OS,))
    def test_chrome_os_not_fn_keys_with_fn_key(self):
        """
        Press on Fn-Key then check if keys that are not F-Keys returned the right key code
        when a Chrome OS has been detected.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Force the switch in Chrome OS mode: long press on fn + c')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.CHROME, duration=ButtonStimuliInterface.LONG_PRESS_DURATION, delay=1)

        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self, excluded_keys=[])

        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)

        for (key_id,) in keys:
            if key_id in fn_keys.values():
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id)
        # end for

        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos Board
        self.kosmos.sequencer.play_sequence(block=False)

        for (key_id,) in keys:
            if key_id in fn_keys.values():
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID Keyboard report for each keys')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.CHROME)

            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.CHROME)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_MEMB_0042")
    # end def test_chrome_os_not_fn_keys_with_fn_key
# end class KeyCodeFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
