#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.ghostkeys.functionality
:brief: Hid Keyboard ghost keys functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/06/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.ghostkeys.ghostkeys import GhostKeysTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class GhostKeysFunctionalityTestCase(GhostKeysTestCase):
    """
    Validates Keyboard Ghost Keys functionality TestCases
    """

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT,))
    def test_group_of_2_keys_with_left_shift(self):
        """
        Check keeping Left Shift key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift'
                                 'key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0001")
    # end def test_group_of_2_keys_with_left_shift

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL,))
    def test_group_of_2_keys_with_left_ctrl(self):
        """
        Check keeping Left Control key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control key is already '
                                 'pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0002")
    # end def test_group_of_2_keys_with_left_ctrl

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_gui(self):
        """
        Check keeping Left Gui key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left gui key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION],
                                                    group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0003")
    # end def test_group_of_2_keys_with_left_gui

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_group_of_2_keys_with_left_alt(self):
        """
        Check keeping Left Alt key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left alt key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_ALT],
                                                    group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0004")
    # end def test_group_of_2_keys_with_left_alt

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_group_of_2_keys_with_right_alt(self):
        """
        Check keeping Right Alt key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right alt key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_ALT],
                                                    group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0005")
    # end def test_group_of_2_keys_with_right_alt

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_right_gui(self):
        """
        Check keeping Right Gui key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right gui key is already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
                                                    group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0006")
    # end def test_group_of_2_keys_with_right_gui

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_right_ctrl(self):
        """
        Check keeping Right Control key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right control key is already '
                                 'pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0007")
    # end def test_group_of_2_keys_with_right_ctrl

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_right_shift(self):
        """
        Check keeping Right Shift key pressed down + 2 other keys pressed simultaneously for all available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right shift key is already '
                                 'pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0008")
    # end def test_group_of_2_keys_with_right_shift

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL,))
    def test_group_of_2_keys_with_left_shift_left_ctrl(self):
        """
        Check keeping Left Shift & Left Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the left control '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_CONTROL], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0010")
    # end def test_group_of_2_keys_with_left_shift_left_ctrl

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_shift_left_gui(self):
        """
        Check keeping Left Shift & Left Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the left gui keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0011")
    # end def test_group_of_2_keys_with_left_shift_left_gui

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_group_of_2_keys_with_left_shift_left_alt(self):
        """
        Check keeping Left Shift & Left Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the left alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_LEFT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0012")
    # end def test_group_of_2_keys_with_left_shift_left_alt

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_group_of_2_keys_with_left_shift_right_alt(self):
        """
        Check keeping Left Shift & Right Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the right alt '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0013")
    # end def test_group_of_2_keys_with_left_shift_right_alt

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_shift_right_gui(self):
        """
        Check keeping Left Shift & Right Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the right gui '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0014")
    # end def test_group_of_2_keys_with_left_shift_right_gui

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_left_shift_right_ctrl(self):
        """
        Check keeping Left Shift & Right Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the right control '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0015")
    # end def test_group_of_2_keys_with_left_shift_right_ctrl

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_left_shift_right_shift(self):
        """
        Check keeping Left Shift & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left shift and the right shift '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_SHIFT, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2, delay=8)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0016")
    # end def test_group_of_2_keys_with_left_shift_right_shift

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_ctrl_left_gui(self):
        """
        Check keeping Left Control & Left Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left ctrl and the left gui keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0020")
    # end def test_group_of_2_keys_with_left_ctrl_left_gui

    @features('Keyboard')
    @features('GhostKeys')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_group_of_2_keys_with_left_ctrl_left_alt(self):
        """
        Check keeping Left Control & Left Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left ctrl and the left alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_LEFT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0021")
    # end def test_group_of_2_keys_with_left_ctrl_left_alt

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_group_of_2_keys_with_left_ctrl_right_alt(self):
        """
        Check keeping Left Control & Right Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left ctrl and the right alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0021")
    # end def test_group_of_2_keys_with_left_ctrl_right_alt

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_ctrl_right_gui(self):
        """
        Check keeping Left Control & Right Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left ctrl and the right gui keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0023")
    # end def test_group_of_2_keys_with_left_ctrl_right_gui

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_left_ctrl_right_ctrl(self):
        """
        Check keeping Left Control & Right Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left ctrl and the right ctrl '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL, right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0024")
    # end def test_group_of_2_keys_with_left_ctrl_right_ctrl

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_left_ctrl_right_shift(self):
        """
        Check keeping Left Control & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left ctrl and the right shift '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0025")
    # end def test_group_of_2_keys_with_left_ctrl_right_shift

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_LEFT_ALT,))
    def test_group_of_2_keys_with_left_gui_left_alt(self):
        """
        Check keeping Left Gui & Left Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left gui and the left alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_LEFT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0030")
    # end def test_group_of_2_keys_with_left_gui_left_alt

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_group_of_2_keys_with_left_gui_right_alt(self):
        """
        Check keeping Left Gui & Right Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left gui and the right alt keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0031")
    # end def test_group_of_2_keys_with_left_gui_right_alt

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_gui_right_gui(self):
        """
        Check keeping Left Gui & Right Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left gui and the right gui keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
            group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0032")
    # end def test_group_of_2_keys_with_left_gui_right_gui

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_left_gui_right_ctrl(self):
        """
        Check keeping Left Gui & Right Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left gui and the right ctrl keys '
                                 'are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0033")
    # end def test_group_of_2_keys_with_left_gui_right_ctrl

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_left_gui_right_shift(self):
        """
        Check keeping Left Gui & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left gui and the right shift '
                                 'keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0034")
    # end def test_group_of_2_keys_with_left_gui_right_shift

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_ALT,))
    def test_group_of_2_keys_with_left_alt_right_alt(self):
        """
        Check keeping Left Alt & Right Alt keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left alt '
                                 'and the right alt keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_ALT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0040")
    # end def test_group_of_2_keys_with_left_alt_right_alt

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_left_alt_right_gui(self):
        """
        Check keeping Left Alt & Right Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left alt '
                                 'and the right gui keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
            group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0041")
    # end def test_group_of_2_keys_with_left_alt_right_gui

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_left_alt_right_ctrl(self):
        """
        Check keeping Left Alt & Right Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left alt '
                                 'and the right ctrl keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_ALT, right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0042")
    # end def test_group_of_2_keys_with_left_alt_right_ctrl

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_left_alt_right_shift(self):
        """
        Check keeping Left Alt & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left alt '
                                 'and the right shift keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_ALT, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0043")
    # end def test_group_of_2_keys_with_left_alt_right_shift

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    def test_group_of_2_keys_with_right_alt_right_gui(self):
        """
        Check keeping Right Alt & Right Gui keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right alt '
                                 'and the right gui keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION],
            group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0050")
    # end def test_group_of_2_keys_with_right_alt_right_gui

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_ALT,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_right_alt_right_ctrl(self):
        """
        Check keeping Right Alt & Right Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right alt '
                                 'and the right ctrl keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_ALT, right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0051")
    # end def test_group_of_2_keys_with_right_alt_right_ctrl

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_right_alt_right_shift(self):
        """
        Check keeping Right Alt & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right alt '
                                 'and the right shift keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_ALT, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0052")
    # end def test_group_of_2_keys_with_right_alt_right_shift

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_right_gui_right_ctrl(self):
        """
        Check keeping Right Gui & Right Control keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right gui'
                                 'and the right ctrl keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION, right_ctrl_key_id], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0060")
    # end def test_group_of_2_keys_with_right_gui_right_ctrl

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    def test_group_of_2_keys_with_right_gui_right_shift(self):
        """
        Check keeping Right Gui & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right gui'
                                 'and the right shift keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0061")
    # end def test_group_of_2_keys_with_right_gui_right_shift

    @features('Keyboard')
    @features("GhostKeys")
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_SHIFT,))
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
    def test_group_of_2_keys_with_right_ctrl_right_shift(self):
        """
        Check keeping Right Control & Right Shift keys pressed down + 2 other keys pressed simultaneously for all
        available key codes
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right ctrl'
                                 'and the right shift keys are already pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(
            self, modifier_key_ids=[right_ctrl_key_id, KEY_ID.KEYBOARD_RIGHT_SHIFT], group_size=2)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0, obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_GHOST_0070")
    # end def test_group_of_2_keys_with_right_ctrl_right_shift
# end class GhostKeysFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
