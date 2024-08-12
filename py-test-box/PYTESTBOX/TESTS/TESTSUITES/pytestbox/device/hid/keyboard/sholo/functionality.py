#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.sholo.functionality
:brief: Hid Keyboard short / long key press detection functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/07/28
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import float_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hid.keyboard.sholo.sholo import SholoTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SholoFunctionalityTestCase(SholoTestCase):
    """
    Validate Keyboard Sholo functionality TestCases.
    """
    TESTED_RANGE = 0.2  # +/- 200ms
    LONG_PRESS_RANGE_START = ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION - TESTED_RANGE
    LONG_PRESS_RANGE_END = ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + TESTED_RANGE
    LONG_PRESS_RANGE_STEP = TESTED_RANGE / 5

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WINDOWS, MultiPlatform.OsMask.MAC_OS,))
    def test_range_less_than_sholo_threshold(self):
        """
        Check keyboard 'o' key pressed less than the OS layout selection threshold is considered as a short press
        if the duration is in the range down to 200ms below the threshold.
        """
        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_id = fn_keys[KEY_ID.FN_KEYBOARD_ENTER]

        for long_press_duration in float_range(SholoFunctionalityTestCase.LONG_PRESS_RANGE_START,
                                               ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION,
                                               SholoFunctionalityTestCase.LONG_PRESS_RANGE_STEP):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate the shortcut to enter in mac os mode (long press on fn + o) '
                                     f'but with a key press duration = {long_press_duration}')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            KeyMatrixTestUtils.emulate_os_shortcut(test_case=self, os_type=OS.MAC, duration=float(long_press_duration))

            self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)

            self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                               delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # Switch back in windows mode: long press on fn + p
            KeyMatrixTestUtils.emulate_os_shortcut(test_case=self)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(timeout=120)

        for _ in float_range(SholoFunctionalityTestCase.LONG_PRESS_RANGE_START,
                             ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION,
                             SholoFunctionalityTestCase.LONG_PRESS_RANGE_STEP):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the O key press is reported normally')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_O, MAKE),
                                                          variant=OS.WINDOWS)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_O, BREAK),
                                                          variant=OS.WINDOWS)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID Keyboard reports in windows os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, MAKE), variant=OS.WINDOWS)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id, BREAK), variant=OS.WINDOWS)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_SHOLO_0001")
    # end def test_range_less_than_sholo_threshold

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WINDOWS, MultiPlatform.OsMask.MAC_OS,))
    def test_range_longer_than_sholo_threshold(self):
        """
        Check keyboard 'o' key pressed longer than the OS layout selection threshold is considered as a long press
        if the duration is in the range up to 200ms above the threshold.
        """
        self.kosmos.sequencer.offline_mode = True
        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_id = fn_keys[KEY_ID.FN_KEYBOARD_ENTER]

        for long_press_duration in float_range(
                ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoFunctionalityTestCase.LONG_PRESS_RANGE_STEP,
                SholoFunctionalityTestCase.LONG_PRESS_RANGE_END, SholoFunctionalityTestCase.LONG_PRESS_RANGE_STEP):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Emulate the shortcut to enter in mac os mode (long press on fn + o) '
                                     f'but with a key press duration = {long_press_duration}')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            KeyMatrixTestUtils.emulate_os_shortcut(test_case=self, os_type=OS.MAC, duration=float(long_press_duration))

            self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)

            self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                               delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # Switch back in windows mode: long press on fn + p
            KeyMatrixTestUtils.emulate_os_shortcut(test_case=self)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(timeout=120)

        for _ in float_range(
                ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoFunctionalityTestCase.LONG_PRESS_RANGE_STEP,
                SholoFunctionalityTestCase.LONG_PRESS_RANGE_END, SholoFunctionalityTestCase.LONG_PRESS_RANGE_STEP):

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID Keyboard reports in mac os mode')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(KEY_ID.FN_KEYBOARD_ENTER, MAKE),
                                                          variant=OS.MAC)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(KEY_ID.FN_KEYBOARD_ENTER, BREAK),
                                                          variant=OS.MAC)
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')

        self.testCaseChecked("FUN_SHOLO_0002")
    # end def test_range_longer_than_sholo_threshold

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_duration_less_than_sholo_threshold_sleep_mode(self):
        """
        Check keyboard 'o' key pressed less than the OS layout selection threshold is considered as a short press
        when the device is in sleep mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)

        self.kosmos.sequencer.offline_mode = True

        # Force the switch in macOS mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION - SholoTestCase.FIVE_MS_MARGIN)

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

        self.testCaseChecked("FUN_SHOLO_0003")
    # end def test_duration_less_than_sholo_threshold_sleep_mode

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_duration_longer_than_sholo_threshold_sleep_mode(self):
        """
        Check keyboard 'o' key pressed longer than the OS layout selection threshold is considered as a long press
        when the device is in sleep mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Wait for the device to enter sleep mode')
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.f.PRODUCT.DEVICE.F_MaxWaitSleep + 1)

        self.kosmos.sequencer.offline_mode = True

        # Force the switch in macOS mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoTestCase.FIVE_MS_MARGIN)

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

        self.testCaseChecked("FUN_SHOLO_0004")
    # end def test_duration_longer_than_sholo_threshold_sleep_mode

    @features('SwitchLatency')
    @features('Feature1830powerMode', 3)
    @features('NoForMAC')
    @level('Functionality')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    @services('KeyMatrix')
    def test_duration_less_than_sholo_threshold_deep_sleep_mode(self):
        """
        Check key pressed less than 2s is considered as a short press when the device is in deep sleep mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        # Force the switch in macOS mode: long press on fn + o
        self.post_requisite_reload_nvs = True
        KeyMatrixTestUtils.emulate_os_shortcut(
            test_case=self, os_type=OS.MAC,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION - SholoTestCase.FIVE_MS_MARGIN)

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

        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)

        self.testCaseChecked("FUN_SHOLO_0005")
    # end def test_duration_less_than_sholo_threshold_deep_sleep_mode

    @features('Keyboard')
    @features('Sholo')
    @features('Feature1830powerMode', 3)
    @features('NoForMAC')
    @level('Functionality')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.MAC_OS,))
    def test_duration_longer_than_sholo_threshold_deep_sleep_mode(self):
        """
        Check key pressed longer than 2s is considered as a long press when the device is in deep sleep mode.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send SetPowerMode with powerModeNumber = 3')
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        self.kosmos.sequencer.offline_mode = True

        # Force the switch in macOS mode: long press on fn + o
        # Add 200ms delay between Fn and O keystroke
        self.post_requisite_reload_nvs = True
        self.button_stimuli_emulator.multiple_keys_press(
            key_ids=[KEY_ID.FN_KEY], delay=ButtonStimuliInterface.DEFAULT_DURATION)
        self.button_stimuli_emulator.keystroke(
            key_id=KEY_ID.KEYBOARD_O,
            duration=ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoTestCase.FIVE_MS_MARGIN,
            delay=KeyMatrixTestUtils.TEN_MS)
        self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY])

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

        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)

        self.testCaseChecked("FUN_SHOLO_0006")
    # end def test_duration_longer_than_sholo_threshold_deep_sleep_mode
# end class SholoFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
