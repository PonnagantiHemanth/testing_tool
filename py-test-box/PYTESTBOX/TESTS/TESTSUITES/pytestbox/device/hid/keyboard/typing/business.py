#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.typing.business
:brief: Hid Keyboard Typing business test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.typing.typing import TypingTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TypingBusinessTestCase(TypingTestCase):
    """
    Validate Keyboard Typing business TestCases
    """

    @features('Keyboard')
    @features('EvtTyping')
    @level('Business')
    @services('KeyMatrix')
    def test_normal_typing_by_key_id_short_version(self):
        """
        FWQA "Normal typing" test short version

        typing scheme = random
        typing period = 1200 ms
        typing period standard deviation = 2000 ms
        make duration = 125 ms
        make duration standard deviation = 90 ms
        repetition = 100
        """
        repetition = 100
        keys_count = 10
        key_id_list = self.build_key_list_adaptive_period(
            make_duration_min=80, make_duration_max=170, delay_min=120, delay_max=2030,
            random_keys_count=keys_count)

        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(repetition=repetition//keys_count, block=True)

        for _ in range(repetition//keys_count):
            for (key_id, ) in key_id_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard report on key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
            # end for
        # end for

        self.testCaseChecked("BUS_TYPG_0001")
    # end def test_normal_typing_by_key_id_short_version

    @features('Keyboard')
    @features('EvtTyping')
    @level('Business')
    @services('KeyMatrix')
    def test_fast_typing_by_key_id_short_version(self):
        """
        FWQA "Fast typing" test short version

        typing scheme = random
        typing period = 50 ms
        typing period standard deviation = 20 ms
        make duration = 35 ms
        make duration standard deviation = 10 ms
        repetition = 100
        """
        repetition = 100
        keys_count = 20
        key_id_list = self.build_key_list_adaptive_period(
            make_duration_min=12, make_duration_max=20, delay_min=32, delay_max=44,
            random_keys_count=keys_count)

        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(repetition=repetition//keys_count, block=True)

        for _ in range(repetition//keys_count):
            for (key_id, ) in key_id_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard report on key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
            # end for
        # end for

        self.testCaseChecked("BUS_TYPG_0002")
    # end def test_fast_typing_by_key_id_short_version
# end class TypingBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
