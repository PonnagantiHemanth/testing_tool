#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.sholo.business
:brief: Hid Keyboard sholo business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/07/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.sholo.sholo import SholoTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SholoBusinessTestCase(SholoTestCase):
    """
    Validate Keyboard Sholo business TestCases
    """
    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Business')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_shortcut_key_pressed_less_than_sholo_threshold(self):
        """
        Check keyboard 'o' key pressed less than the OS layout selection threshold is considered as a short press.
        """
        self.kosmos.sequencer.offline_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate the shortcut to enter in mac os mode (long press on fn + o) '
                                 'but with a key press duration shorter than the 2s threshold')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION - SholoTestCase.FIVE_MS_MARGIN,
            delay=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION)

        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_id = fn_keys[KEY_ID.FN_KEYBOARD_ENTER]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)

        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the O key press is reported normally')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_O, MAKE),
                                                      variant=OS.WINDOWS)

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_O, BREAK),
                                                      variant=OS.WINDOWS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID Keyboard reports in windows os mode')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.WINDOWS)

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.WINDOWS)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_SHOLO_0001")
    # end def test_mac_shortcut_key_pressed_less_than_sholo_threshold

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Business')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_mac_shortcut_key_pressed_longer_than_sholo_threshold(self):
        """
        Check keyboard 'o' key pressed longer than the OS layout selection threshold is considered as a long press.
        """
        self.kosmos.sequencer.offline_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate the shortcut to enter in mac os mode (long press on fn + o) '
                                 'but with a key press duration longer than the 2s threshold')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoTestCase.FIVE_MS_MARGIN,
            delay=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION)

        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_id = fn_keys[KEY_ID.FN_KEYBOARD_ENTER]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)

        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                           delay=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID Keyboard reports in mac os mode')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.FN_KEYBOARD_ENTER, MAKE),
                                                      variant=OS.MAC)

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.FN_KEYBOARD_ENTER, BREAK),
                                                      variant=OS.MAC)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_SHOLO_0002")
    # end def test_mac_shortcut_key_pressed_longer_than_sholo_threshold

    @features('Keyboard')
    @features('Sholo')
    @features('ForMAC')
    @level('Business')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DO_NOT_DISTURB, KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    def test_ipad_shortcut_key_pressed_less_than_sholo_threshold(self):
        """
        Check keyboard 'i' key pressed less than the OS layout selection threshold is considered as a short press.

        Note that we are leveraging the 'Do not disturb' key which has a different translation between Mac and Ipad
        modes to verify the shortcut processing.
        """
        self.kosmos.sequencer.offline_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate the shortcut to enter in ipad os mode (long press on fn + i) '
                                 'but with a key press duration shorter than the expected threshold')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.IPAD,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION - SholoTestCase.FIVE_MS_MARGIN,
            delay=ButtonStimuliInterface.LONG_PRESS_DURATION)

        key_id = KEY_ID.DO_NOT_DISTURB
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=key_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Return in mac os mode: long press on fn + o')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the I key press is reported normally')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_I, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_I, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID Keyboard reports in mac os mode')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_SHOLO_0003")
    # end def test_ipad_shortcut_key_pressed_less_than_sholo_threshold

    @features('Keyboard')
    @features('Sholo')
    @features('ForMAC')
    @level('Business')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.DO_NOT_DISTURB, KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    def test_ipad_shortcut_key_pressed_longer_than_sholo_threshold(self):
        """
        Check keyboard 'i' key pressed longer than the OS layout selection threshold is considered as a long press.

        Note that we are leveraging the 'Do not disturb' key which has a different translation between Mac and Ipad
        modes to verify the shortcut processing.
        """
        self.kosmos.sequencer.offline_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate the shortcut to enter in ipad os mode (long press on fn + i) '
                                 'but with a key press duration shorter than the expected threshold')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.IPAD,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoTestCase.FIVE_MS_MARGIN,
            delay=ButtonStimuliInterface.LONG_PRESS_DURATION)

        key_id = KEY_ID.DO_NOT_DISTURB
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on the key {str(key_id)}')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=key_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Return in mac os mode: long press on fn + o')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check HID Keyboard reports in ipad os mode')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                      variant=OS.IPAD)

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                      variant=OS.IPAD)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("BUS_SHOLO_0004")
    # end def test_ipad_shortcut_key_pressed_longer_than_sholo_threshold
# end class SholoBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
