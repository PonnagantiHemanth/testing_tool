#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.sholo.robustness
:brief: Hid Keyboard short / long key press detection Robustness test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/10/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import OS
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatform
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import float_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.sholo.sholo import SholoTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SholoRobustnessTestCase(SholoTestCase):
    """
    Validate Keyboard Sholo Robustness TestCases for NPI reports
    """
    TESTED_RANGE = 0.2  # +/- 200ms
    LONG_PRESS_RANGE_START = ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION - TESTED_RANGE
    LONG_PRESS_RANGE_END = ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + TESTED_RANGE
    LONG_PRESS_RANGE_STEP = TESTED_RANGE / 5
    LOOPS_PER_ITEM = 50

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Robustness')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WINDOWS, MultiPlatform.OsMask.MAC_OS,))
    def test_below_sholo_threshold_stats(self):
        """
        Perform steps to generate stats below the expected sholo threshold:
            - loop for the specific durations below sholo threshold
            -   clear the pass count
            -   loop for the specific count
            -     check heck keyboard 'o' key pressed less than the OS layout selection threshold
            -       is considered as a short press
            -     if passed then increase the pass count
            -   end for loop
            -   calculate and log the pass rate for the specific duration
            - end for loop
        """
        self.post_requisite_reload_nvs = True

        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_id = fn_keys[KEY_ID.FN_KEYBOARD_ENTER]

        pass_status = True

        for long_press_duration in float_range(SholoRobustnessTestCase.LONG_PRESS_RANGE_START,
                                               ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION,
                                               SholoRobustnessTestCase.LONG_PRESS_RANGE_STEP):
            pass_count = 0
            for _ in range(SholoRobustnessTestCase.LOOPS_PER_ITEM):
                self.missing_hid_report_counter = 0
                self.kosmos.sequencer.offline_mode = True
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Emulate the shortcut to enter in mac os mode (long press on fn + o) '
                                         f'but with a key press duration = {long_press_duration}')
                # ------------------------------------------------------------------------------------------------------

                KeyMatrixTestUtils.emulate_os_shortcut(
                    test_case=self, os_type=OS.MAC, duration=float(long_press_duration))

                self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY],
                                                                 delay=ButtonStimuliInterface.DEFAULT_DURATION)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)

                self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                                   delay=ButtonStimuliInterface.DEFAULT_DURATION)

                # Switch back in windows mode: long press on fn + p
                KeyMatrixTestUtils.emulate_os_shortcut(test_case=self)

                self.kosmos.sequencer.offline_mode = False
                # Upload the complete scenario into the Kosmos
                self.kosmos.sequencer.play_sequence(timeout=120)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check the O key press is reported normally')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_O, MAKE),
                                                              variant=OS.WINDOWS,
                                                              raise_exception=False)

                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_O, BREAK),
                                                              variant=OS.WINDOWS,
                                                              raise_exception=False)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check HID Keyboard reports in windows os mode')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                              variant=OS.WINDOWS,
                                                              raise_exception=False)

                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                              variant=OS.WINDOWS,
                                                              raise_exception=False)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Verify no HID report was missing')
                # ------------------------------------------------------------------------------------------------------
                if KeyMatrixTestUtils.get_missing_report_counter(self) == 0:
                    pass_count = pass_count + 1
                # end if
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_metrics(test_case=self,
                                  key=f'Press duration:{long_press_duration}, Pass rate:',
                                  value=f'{pass_count * 100 / SholoRobustnessTestCase.LOOPS_PER_ITEM}%')
            # ----------------------------------------------------------------------------------------------------------
            if pass_count != SholoRobustnessTestCase.LOOPS_PER_ITEM:
                pass_status = False
            # end if
        # end for

        self.assertTrue(pass_status, msg='Some HID reports were missing')

        self.testCaseChecked("ROB_SHOLO_0001")
    # end def test_below_sholo_threshold_stats

    @features('Keyboard')
    @features('Sholo')
    @features('NoForMAC')
    @level('Robustness')
    @services('KeyMatrix')
    @services('RequiredKeys', (KEY_ID.KEYBOARD_RETURN_ENTER, KEY_ID.KEYBOARD_O,))
    @services("RequiredOsLayout", (MultiPlatform.OsMask.WINDOWS, MultiPlatform.OsMask.MAC_OS,))
    def test_above_sholo_threshold_stats(self):
        """
        Perform steps to generate stats above the expected sholo threshold:
            - loop for the specific durations above sholo threshold
            -   clear the pass count
            -   loop for the specific count
            -     check keyboard 'o' key pressed longer than the OS layout selection threshold
            -       is considered as a long press
            -     if passed then increase the pass count
            -   end for loop
            -   calculate and log the pass rate for the specific duration
            - end for loop
        """
        self.post_requisite_reload_nvs = True

        fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
        key_id = fn_keys[KEY_ID.FN_KEYBOARD_ENTER]

        pass_status = True

        for long_press_duration in float_range(
                ButtonStimuliInterface.OS_LAYOUT_SELECTION_DURATION + SholoRobustnessTestCase.LONG_PRESS_RANGE_STEP,
                SholoRobustnessTestCase.LONG_PRESS_RANGE_END,
                SholoRobustnessTestCase.LONG_PRESS_RANGE_STEP):
            pass_count = 0
            for _ in range(SholoRobustnessTestCase.LOOPS_PER_ITEM):
                self.missing_hid_report_counter = 0
                self.kosmos.sequencer.offline_mode = True
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Emulate the shortcut to enter in mac os mode (long press on fn + o) '
                                         f'but with a key press duration = {long_press_duration}')
                # ------------------------------------------------------------------------------------------------------

                KeyMatrixTestUtils.emulate_os_shortcut(test_case=self, os_type=OS.MAC,
                                                       duration=float(long_press_duration))

                self.button_stimuli_emulator.multiple_keys_press(key_ids=[KEY_ID.FN_KEY], delay=1)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(key_id=key_id, repeat=1)

                self.button_stimuli_emulator.multiple_keys_release(key_ids=[KEY_ID.FN_KEY],
                                                                   delay=ButtonStimuliInterface.DEFAULT_DURATION)

                # Switch back in windows mode: long press on fn + p
                KeyMatrixTestUtils.emulate_os_shortcut(test_case=self)

                self.kosmos.sequencer.offline_mode = False
                # Upload the complete scenario into the Kosmos
                self.kosmos.sequencer.play_sequence(timeout=120)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check HID Keyboard reports in mac os mode')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(KEY_ID.FN_KEYBOARD_ENTER, MAKE), variant=OS.MAC,
                    raise_exception=False)

                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(KEY_ID.FN_KEYBOARD_ENTER, BREAK), variant=OS.MAC,
                    raise_exception=False)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Verify no HID report was missing')
                # ------------------------------------------------------------------------------------------------------
                if KeyMatrixTestUtils.get_missing_report_counter(self) == 0:
                    pass_count = pass_count + 1
                # end if
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_metrics(test_case=self,
                                  key=f'Press duration:{long_press_duration}, Pass rate:',
                                  value=f'{pass_count * 100 / SholoRobustnessTestCase.LOOPS_PER_ITEM}%')
            # ----------------------------------------------------------------------------------------------------------
            if pass_count != SholoRobustnessTestCase.LOOPS_PER_ITEM:
                pass_status = False
            # end if
        # end for

        self.assertTrue(pass_status, msg='Some HID reports were missing')

        self.testCaseChecked("ROB_SHOLO_0002")
    # end def test_above_sholo_threshold_stats
# end class SholoRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
