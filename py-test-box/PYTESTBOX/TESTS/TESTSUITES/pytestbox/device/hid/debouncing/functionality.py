#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.debouncing.functionality
:brief: Hid debouncing functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddata import HidData
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hid.debouncing.debouncing import DebouncingTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DebouncingFunctionalityTestCase(DebouncingTestCase):
    """
    Validate Debouncing functionality TestCases
    """
    LOOP_COUNT = 2

    @features('Debounce')
    @level('Functionality')
    @services('ButtonPressed')
    def test_100percent_make_sleep_mode(self):
        """
        Check the timing defined in the FW specification above which a make shall always occur (100% Make)
        """
        self.kosmos.sequencer.offline_mode = True
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        sleep_mode_time = self.f.PRODUCT.DEVICE.F_MaxWaitSleep
        # Add a DELAY instruction matching the time needed for the device to enter sleep mode
        self.kosmos.pes.delay(delay_s=sleep_mode_time)

        for index in range(self.LOOP_COUNT):
            make_duration = self.f.PRODUCT.DEBOUNCE.F_100PercentMakeDebounceUs
            delay = sleep_mode_time if index < self.LOOP_COUNT - 1 else ButtonStimuliInterface.DEFAULT_DURATION

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke with duration of the make = {make_duration}us')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=make_duration / 10**6, delay=delay)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(self, f'Wait {delay}s to let the device re-enter sleep mode')
            # ---------------------------------------------------------------------------
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # Wait enough time for the whole scenario to be executed
        sleep(self.LOOP_COUNT * sleep_mode_time)

        for _ in range(self.LOOP_COUNT):
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check a make has been detected and generate an HID report')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the release also generate an HID report')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        self.testCaseChecked("FUN_DEBC_0001")
    # end def test_100percent_make_sleep_mode

    @features('Debounce')
    @level('Functionality')
    @services('ButtonPressed')
    def test_100percent_break_sleep_mode(self):
        """
        Check the timing defined in the FW specification above which a break shall always occur (100% Break)
        """
        self.kosmos.sequencer.offline_mode = True
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=False,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        sleep_mode_time = self.f.PRODUCT.DEVICE.F_MaxWaitSleep

        for index in range(self.LOOP_COUNT):
            break_duration = self.f.PRODUCT.DEBOUNCE.F_100PercentBreakDebounceUs
            # ---------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Keep the key pressed for {sleep_mode_time}s to let the device re-enter sleep mode then '
                      f'release the key for = {break_duration}us')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=sleep_mode_time,
                                                   delay=break_duration / 10**6)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # Wait enough time for the whole scenario to be executed
        sleep(self.LOOP_COUNT * sleep_mode_time)

        for _ in range(self.LOOP_COUNT):
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check a make has been detected and generate an HID report')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the release also generate an HID report')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for

        self.testCaseChecked("BUS_DEBC_0002")
    # end def test_100percent_break_sleep_mode

    @features('Debounce')
    @features('Feature1830powerMode', 3)
    @level('Functionality')
    @services('ButtonPressed')
    def test_100percent_make_deep_sleep_mode(self):
        """
        Check in deep sleep mode the timing defined in the FW specification above which a make shall always occur
        (100% Make)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device into deep sleep mode thru the 0x1830 SetPowerMode request')
        # ---------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=True,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]

        make_duration = self.f.PRODUCT.DEBOUNCE.F_100PercentMakeDeepSleepUs

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate a keystroke with duration of the make = {make_duration}us')
        # ---------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=make_duration / 10**6)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check a make has been detected and generate an HID report')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the release also generate an HID report')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)

        self.testCaseChecked("FUN_DEBC_0003")
    # end def test_100percent_make_deep_sleep_mode

    @features('Debounce')
    @features('Feature1830powerMode', 3)
    @features('Keyboard')
    @level('Functionality')
    @services('ButtonPressed')
    def test_100percent_break_deep_sleep_mode(self):
        """
        Check in deep sleep mode the timing defined in the FW specification above which a break shall always occur
        (100% Break)
        """
        (key_id, ) = KeyMatrixTestUtils.get_key_list(self, group_count=1, group_size=1, random=True,
                                                     excluded_keys=HidData.get_not_single_action_keys())[0]
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate an immediate key pressed on key id = {str(key_id)}')
        # ---------------------------------------------------------------------------
        self.button_stimuli_emulator.key_press(key_id=key_id)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the first make has been detected and generate an HID report')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Force the device into deep sleep mode thru the 0x1830 SetPowerMode request')
        # ---------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)

        self.kosmos.sequencer.offline_mode = True
        break_duration = self.f.PRODUCT.DEBOUNCE.F_100PercentBreakDebounceUs
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Keep the key released for = {break_duration}us')
        # ---------------------------------------------------------------------------
        self.button_stimuli_emulator.key_release(key_id=key_id)
        # Add a DELAY instruction matching the expected break duration
        self.kosmos.pes.delay(delay_ns=break_duration * 10 ** 3)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Then redo a key press on the exact same key')
        # ---------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION)

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the release also generate an HID report')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the second make is also detected and generate an HID report')
        # ---------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

        ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, class_type=WirelessDeviceStatusBroadcastEvent)

        self.testCaseChecked("FUN_DEBC_0004")
    # end def test_100percent_break_deep_sleep_mode

# end class DebouncingFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
