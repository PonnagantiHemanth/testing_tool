#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.layout.functionality
:brief: Hid Keyboard layout functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.keyboardemulator import KeyboardMixin
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.layoututils import LayoutTestUtils as Utils
from pytestbox.device.hid.keyboard.layout.layout import LayoutTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LayoutFunctionalityTestCase(LayoutTestCase):
    """
    Validate Keyboard Layout functionality TestCases
    """

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SingleKeystroke')
    @services('Debugger')
    def test_uk_layout_all_available_keys(self):
        """
        Check all keys starting returned the correct key code when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_key_code()

        self.testCaseChecked("FUN_LAYT_0001")
    # end def test_uk_layout_all_available_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_left_shift(self):
        """
        Check all keys returned the correct key code if preceded by a left shift key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_left_shift()

        self.testCaseChecked("FUN_LAYT_0002")
    # end def test_uk_layout_all_keys_with_left_shift

    def _test_all_keys_with_left_shift(self):
        """
        Common part of the all available keys with left shift tests.
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
    # end def _test_all_keys_with_left_shift

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_SHIFT,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_right_shift(self):
        """
        Check all keys returned the correct key code if preceded by a right shift key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_right_shift()

        self.testCaseChecked("FUN_LAYT_0003")
    # end def test_uk_layout_all_keys_with_right_shift

    def _test_all_keys_with_right_shift(self):
        """
        Common part of the all available keys with right shift tests.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right shift key is already '
                                 'pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_RIGHT_SHIFT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_all_keys_with_right_shift

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_left_ctrl(self):
        """
        Check all keys returned the correct key code if preceded by a left control key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_left_ctrl()

        self.testCaseChecked("FUN_LAYT_0004")
    # end def test_uk_layout_all_keys_with_left_ctrl

    def _test_all_keys_with_left_ctrl(self):
        """
        Common part of the all available keys with left control key tests.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the left control key is already '
                                 'pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[KEY_ID.KEYBOARD_LEFT_CONTROL])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_all_keys_with_left_ctrl

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('AtLeastOneKey', (KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,),
              KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_right_ctrl(self):
        """
        Check all keys returned the correct key code if preceded by a right control key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_right_ctrl()

        self.testCaseChecked("FUN_LAYT_0005")
    # end def test_uk_layout_all_keys_with_right_ctrl

    def _test_all_keys_with_right_ctrl(self):
        """
        Common part of the all available keys with right control key tests.
        """
        right_ctrl_key_id = KeyMatrixTestUtils.get_first_supported_key_id(
            self, key_ids=(KEY_ID.KEYBOARD_RIGHT_CONTROL, KEY_ID.KEYBOARD_RIGHT_CONTROL_OR_OPTION,))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a keystroke on all supported keys when the right control key is already '
                                 'pressed')
        LogHelper.log_check(self, 'Verify the HID keyboard bitmap reports match their expected values')
        # --------------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.send_keys_with_modifiers(self, modifier_key_ids=[right_ctrl_key_id])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_all_keys_with_right_ctrl

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_ALT,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_left_alt(self):
        """
        Check all keys returned the correct key code if preceded by a left alt key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_left_alt()

        self.testCaseChecked("FUN_LAYT_0006")
    # end def test_uk_layout_all_keys_with_left_alt

    def _test_all_keys_with_left_alt(self):
        """
        Common part of the all keys with left alt key tests.
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
    # end def _test_all_keys_with_left_alt

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_ALT,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_right_alt(self):
        """
        Check all keys returned the correct key code if preceded by a right alt key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_right_alt()

        self.testCaseChecked("FUN_LAYT_0007")
    # end def test_uk_layout_all_keys_with_right_alt

    def _test_all_keys_with_right_alt(self):
        """
        Common part of the all keys with right alt key tests.
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
    # end def _test_all_keys_with_right_alt

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_WIN_OR_OPTION,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_left_win(self):
        """
        Check all keys returned the correct key code if preceded by a left win key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_left_win()

        self.testCaseChecked("FUN_LAYT_0008")
    # end def test_uk_layout_all_keys_with_left_win

    def _test_all_keys_with_left_win(self):
        """
        Common part of the all keys with left win key tests.
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
    # end def _test_all_keys_with_left_win

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_WIN_OR_OPTION,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_all_keys_with_right_win(self):
        """
        Check all keys returned the correct key code if preceded by a right win key press
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_all_keys_with_right_win()

        self.testCaseChecked("FUN_LAYT_0009")
    # end def test_uk_layout_all_keys_with_right_win

    def _test_all_keys_with_right_win(self):
        """
        Common part of the all keys with right win key tests.
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
    # end def _test_all_keys_with_right_win

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services('Debugger')
    def test_uk_layout_not_fn_keys_with_fn_key(self):
        """
        Press on Fn-Key then check if keys that are not F-Keys returned the correct key code
        when the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_not_fn_keys_with_fn_key()

        self.testCaseChecked("FUN_LAYT_0010")
    # end def test_uk_layout_not_fn_keys_with_fn_key

    def _test_not_fn_keys_with_fn_key(self):
        """
        Common part of the keys that are not F-Keys tests.
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
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)
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
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_not_fn_keys_with_fn_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_uk_layout_mac_os_all_keys(self):
        """
        Check all FW key codes are correct when a macOS has been selected and the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_mac_os_all_keys()

        self.testCaseChecked("FUN_LAYT_0011")
    # end def test_uk_layout_mac_os_all_keys

    def _test_mac_os_all_keys(self):
        """
        Common part of the all available keys tests in macOS mode.
        """
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)

        # Force the switch in macOS mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in macOS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_mac_os_all_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_uk_layout_mac_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when a macOS has been selected
        and the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_mac_os_fn_keys()

        self.testCaseChecked("FUN_LAYT_0012")
    # end def test_uk_layout_mac_os_fn_keys

    def _test_mac_os_fn_keys(self):
        """
        Common part of the Fn keys tests in macOS mode.
        """
        self.post_requisite_reload_nvs = True
        # Force the switch in macOS mode: long press on fn + o
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION, delay=1)

        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Emulate a key press on Fn-Key')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                         delay=ButtonStimuliInterface.DEFAULT_DURATION)
        assert self.button_stimuli_emulator.fn_pressed, 'FN key has not been correctly pressed !'

        for key_id in iter(fn_keys.values()):
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
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in macOS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_mac_os_fn_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('Debugger')
    def test_uk_layout_mac_os_not_fn_keys_with_fn_key(self):
        """
        Press on Fn-Key then check if keys that are not F-Keys returned the right key code
        when a macOS has been selected and the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_mac_os_not_fn_keys_with_fn_key()

        self.testCaseChecked("FUN_LAYT_0013")
    # end def test_uk_layout_mac_os_not_fn_keys_with_fn_key

    def _test_mac_os_not_fn_keys_with_fn_key(self):
        """
        Common part of the keys that are not F-Keys tests in macOS mode.
        """
        self.post_requisite_reload_nvs = True
        # Force the switch in macOS mode: long press on fn + o
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
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)
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
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_mac_os_not_fn_keys_with_fn_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_uk_layout_ipad_os_all_keys(self):
        """
        Check all FW key codes are correct when an iPadOS has been selected and the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_ipad_os_all_keys()

        self.testCaseChecked("FUN_LAYT_0014")
    # end def test_uk_layout_ipad_os_all_keys

    def _test_ipad_os_all_keys(self):
        """
        Common part of the Fn keys tests in iPadOS mode.
        """
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)

        self.post_requisite_reload_nvs = True
        # Force the switch in iPadOS mode: long press on fn + i
        KeyMatrixTestUtils.emulate_os_shortcut(test_case=self, os_type=OS.IPAD,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1, duration=1)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)
        sleep(ButtonStimuliInterface.LONG_PRESS_DURATION)

        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in iPadOS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.IPAD)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.IPAD)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_ipad_os_all_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_uk_layout_ipad_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when an iPadOS has been selected
        and the UK layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_ipad_os_fn_keys()

        self.testCaseChecked("FUN_LAYT_0015")
    # end def test_uk_layout_ipad_os_fn_keys

    def _test_ipad_os_fn_keys(self):
        """
        Common part of the Fn keys tests in iPadOS mode.
        """
        self.post_requisite_reload_nvs = True
        # Force the switch in iPadOS mode: long press on fn + i
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

        for key_id in iter(fn_keys.values()):
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
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in iPadOS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.IPAD)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.IPAD)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_ipad_os_fn_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_NO_US_1, KEY_ID.KEYBOARD_NO_US_45), KeyboardMixin.LAYOUT.ISO_105_KEY)
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('Debugger')
    def test_uk_layout_inverted_mac_os_keys(self):
        """
        Check the keyboard shortcut Fn+U (long press) that will activate the option of having standard HID codes 0x35
        and 0x64 for these two keys when the UK layout is configured.
        It will work as a toggle, by default these two HID key codes are inverted,
        then after Fn+U they won't be inverted.
        Again if Fn+U is pressed, two keys get again inverted.

        cf OS Selection User Experience 1.2.6:
        https://docs.google.com/document/d/1v0dRllFLLaG0icASJuB_266Gqoch8SnHCwxDUTWw1L4/edit#
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to UK")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.UK)

        self._test_inverted_mac_os_keys()

        self.testCaseChecked("FUN_LAYT_0016")
    # end def test_uk_layout_inverted_mac_os_keys

    def _test_inverted_mac_os_keys(self):
        """
        Common part of the standard HID codes 0x35 and 0x64 keys inversion tests in macOS mode.
        """
        # Force the switch in inverted macOS mode: long press on fn + u
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.INVERTED_MAC, duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        self.kosmos.sequencer.offline_mode = True
        for (key_id,) in [(KEY_ID.KEYBOARD_NO_US_1,), (KEY_ID.KEYBOARD_NO_US_45,), ]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)
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
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)} in inverted macOS mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.INVERTED_MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.INVERTED_MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def _test_inverted_mac_os_keys

    # ----- JPN Layout -------------------------------------------------------------------------------------------------
    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SingleKeystroke')
    @services('Debugger')
    def test_jpn_layout_all_available_keys(self):
        """
        Check all keys starting returned the correct key code when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_key_code()

        self.testCaseChecked("FUN_LAYT_0101")
    # end def test_jpn_layout_all_available_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_SHIFT,), KeyboardMixin.LAYOUT.JIS_109_KEY)
    @services('Debugger')
    def test_jpn_layout_all_keys_with_left_shift(self):
        """
        Check all keys returned the correct key code if preceded by a left shift key press
        when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_all_keys_with_left_shift()

        self.testCaseChecked("FUN_LAYT_0102")
    # end def test_jpn_layout_all_keys_with_left_shift

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RIGHT_SHIFT,), KeyboardMixin.LAYOUT.JIS_109_KEY)
    @services('Debugger')
    def test_jpn_layout_all_keys_with_right_shift(self):
        """
        Check all keys returned the correct key code if preceded by a right shift key press
        when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_all_keys_with_right_shift()

        self.testCaseChecked("FUN_LAYT_0103")
    # end def test_jpn_layout_all_keys_with_right_shift

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('SimultaneousKeystrokes')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_LEFT_CONTROL,), KeyboardMixin.LAYOUT.JIS_109_KEY)
    @services('Debugger')
    def test_jpn_layout_all_keys_with_left_ctrl(self):
        """
        Check all keys returned the correct key code if preceded by a left control key press
        when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_all_keys_with_left_ctrl()

        self.testCaseChecked("FUN_LAYT_0104")
    # end def test_jpn_layout_all_keys_with_left_ctrl

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.FN_KEY,), KeyboardMixin.LAYOUT.JIS_109_KEY)
    @services('Debugger')
    def test_jpn_layout_not_fn_keys_with_fn_key(self):
        """
        Press on Fn-Key then check if keys that are not F-Keys returned the correct key code
        when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_not_fn_keys_with_fn_key()

        self.testCaseChecked("FUN_LAYT_0105")
    # end def test_jpn_layout_not_fn_keys_with_fn_key

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_jpn_layout_mac_os_all_keys(self):
        """
        Check all FW key codes are correct when a macOS has been selected
        when the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_mac_os_all_keys()

        self.testCaseChecked("FUN_LAYT_0106")
    # end def test_jpn_layout_mac_os_all_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_jpn_layout_mac_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when a macOS has been selected
        and the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_mac_os_fn_keys()

        self.testCaseChecked("FUN_LAYT_0107")
    # end def test_jpn_layout_mac_os_fn_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_jpn_layout_ipad_os_all_keys(self):
        """
        Check all FW key codes are correct when an iPadOS has been selected and the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_ipad_os_all_keys()

        self.testCaseChecked("FUN_LAYT_0108")
    # end def test_jpn_layout_ipad_os_all_keys

    @features('Keyboard')
    @features('Layout')
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.KEYBOARD_LAYOUT)
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_I,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.IOS,))
    @services('SimultaneousKeystrokes')
    @services('Debugger')
    def test_jpn_layout_ipad_os_fn_keys(self):
        """
        Press on Fn-Key then check if the F-keys are returning the right key code when an iPadOS has been selected
        and the japanese layout is configured.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Configure the Keyboard International Layout to JPN")
        # --------------------------------------------------------------------------------------------------------------
        Utils.select_layout(self, layout=KeyboardInternationalLayouts.LAYOUT.JAPANESE)

        self._test_ipad_os_fn_keys()

        self.testCaseChecked("FUN_LAYT_0109")
    # end def test_jpn_layout_ipad_os_fn_keys

# end class LayoutFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
