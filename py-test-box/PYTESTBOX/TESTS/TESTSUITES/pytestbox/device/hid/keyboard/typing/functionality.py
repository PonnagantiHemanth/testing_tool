#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.typing.functionality
:brief: Hid Keyboard Typing functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.device.hid.keyboard.typing.typing import TypingTestCase
from pytestbox.tools.reportgenerator.config.evt_typing import EvtTypingConfig


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TypingFunctionalityTestCase(TypingTestCase):
    """
    Validate Keyboard Typing business TestCases
    """

    @features('Keyboard')
    @features('EvtTyping')
    @features('Feature1830powerMode', 3)
    @level('Functionality')
    @services('KeyMatrix')
    def test_wake_up_quick(self):
        """
        FWQA "Wake-up quick" test

        typing scheme = random
        Total number of keys = 3900 (EVT) or 30 (CI)
        key count = 10
        loop = 390 (EVT) or 3 (CI)
        typing period = 1000 ms
        random typing period = 0 ms
        make duration = 80 ms
        random make period = 0 ms
        """
        self.SHEET_CELL_ID = EvtTypingConfig.CellRange.WAKE_UP_QUICK_KEY
        self.SWEEP_MIN = self.WAKE_UP_QUICK_TYPING_SWEEP_MIN
        self.SWEEP_MAX = self.WAKE_UP_QUICK_TYPING_SWEEP_MAX
        self.SWEEP_DEC = self.WAKE_UP_QUICK_TYPING_SWEEP_DEC

        self.check_key_by_hid_code(rep_key_count=self.WAKE_UP_QUICK_KEY_COUNT,
                                   loop_count=self.WAKE_UP_QUICK_LOOPS,
                                   make_duration_min=self.WAKE_UP_QUICK_TYPING_MAKE_DURATION_MIN,
                                   make_duration_max=self.WAKE_UP_QUICK_TYPING_MAKE_DURATION_MAX,
                                   delay_min=self.WAKE_UP_QUICK_TYPING_DELAY_MIN,
                                   delay_max=self.WAKE_UP_QUICK_TYPING_DELAY_MAX,
                                   sleep=True)

        self.testCaseChecked("FUN_TYPG_0001")
    # end def test_wake_up_quick

    @features('Keyboard')
    @features('EvtTyping')
    @features('GamingDevice')
    @level('Time-consuming')
    @services('KeyMatrix')
    def test_gaming(self):
        """
        FWQA "Gaming" test

        typing scheme = random
        Total number of keys = 2000 (EVT) or 30 (CI)
        key count = 10
        loop = 200 (EVT) or 3 (CI)
        typing period = 150 ms
        random typing period = 100 ms
        make duration = 300 ms
        random make period = 0 ms
        """
        self.SHEET_CELL_ID = EvtTypingConfig.CellRange.GAMING_KEY

        self.check_gaming_key_by_hid_code(rep_key_count=self.GAMING_KEY_COUNT,
                                          loop_count=self.GAMING_LOOPS,
                                          make_duration_min=self.GAMING_TYPING_MAKE_DURATION_MIN,
                                          make_duration_max=self.GAMING_TYPING_MAKE_DURATION_MAX,
                                          next_make_at_min=self.GAMING_TYPING_NEXT_MAKE_DURATION_MIN,
                                          next_make_at_max=self.GAMING_TYPING_NEXT_MAKE_DURATION_MAX)

        self.testCaseChecked("FUN_TYPG_0002")
    # end def test_gaming

    @features('Keyboard')
    @features('EvtTyping')
    @features('Feature1830powerMode', 3)
    @level('Functionality')
    @services('KeyMatrix')
    def test_wake_up_slow(self):
        """
        FWQA "wake up slow" test

        typing scheme = random
        Total number of keys = 850 (EVT) or 20 (CI)
        key count = 10
        loop = 85 (EVT) or 2 (CI)
        typing period = 3000 ms
        random typing period = 0 ms
        make duration = 80 ms
        random make period = 0 ms
        """
        self.SHEET_CELL_ID = EvtTypingConfig.CellRange.WAKE_UP_SLOW_KEY
        self.SWEEP_MIN = self.WAKE_UP_SLOW_TYPING_SWEEP_MIN
        self.SWEEP_MAX = self.WAKE_UP_SLOW_TYPING_SWEEP_MAX
        self.SWEEP_DEC = self.WAKE_UP_SLOW_TYPING_SWEEP_DEC

        self.check_key_by_hid_code(rep_key_count=self.WAKE_UP_SLOW_KEY_COUNT,
                                   loop_count=self.WAKE_UP_SLOW_LOOPS,
                                   make_duration_min=self.WAKE_UP_SLOW_TYPING_MAKE_DURATION_MIN,
                                   make_duration_max=self.WAKE_UP_SLOW_TYPING_MAKE_DURATION_MAX,
                                   delay_min=self.WAKE_UP_SLOW_TYPING_DELAY_MIN,
                                   delay_max=self.WAKE_UP_SLOW_TYPING_DELAY_MAX,
                                   sleep=True)

        self.testCaseChecked("FUN_TYPG_0003")
    # end def test_wake_up_slow

    @features('Keyboard')
    @features('EvtTyping')
    @level('Time-consuming')
    @services('KeyMatrix')
    def test_endurance_typing(self):
        """
        FWQA "endurance" test

        typing scheme = random
        Total number of keys = 300000 (EVT) or 100 (CI)
        key count = 10
        loop = 30000 (EVT) or 10 (CI)
        typing period = 130 ms
        random typing period = 140 ms
        make duration = 60 ms
        random make period = 40 ms
        """
        self.SHEET_CELL_ID = EvtTypingConfig.CellRange.ENDURANCE_KEY

        self.check_key_by_hid_code(rep_key_count=self.ENDURANCE_TYPING_KEY_COUNT,
                                   loop_count=self.ENDURANCE_TYPING_LOOPS,
                                   make_duration_min=self.ENDURANCE_TYPING_MAKE_DURATION_MIN,
                                   make_duration_max=self.ENDURANCE_TYPING_MAKE_DURATION_MAX,
                                   delay_min=self.ENDURANCE_TYPING_DELAY_MIN,
                                   delay_max=self.ENDURANCE_TYPING_DELAY_MAX)

        self.testCaseChecked("FUN_TYPG_0004")
    # end def test_endurance_typing

    @features('Keyboard')
    @features('EvtTyping')
    @level('Time-consuming')
    @services('KeyMatrix')
    def test_fast_typing_by_key_id_long_version(self):
        """
        FWQA "Fast typing" test

        typing scheme = random
        Total number of keys = 100000 (EVT) or 100 (CI)
        key count = 10
        loop = 10000 (EVT) or 10 (CI)
        typing period = 50 ms
        random typing period = 20 ms
        make duration = 35 ms
        random make period = 10 ms
        """
        self.SHEET_CELL_ID = EvtTypingConfig.CellRange.FAST_TYPING_KEY

        self.check_key_by_hid_code(rep_key_count=self.FAST_TYPING_KEY_COUNT,
                                   loop_count=self.FAST_TYPING_LOOPS,
                                   make_duration_min=self.FAST_TYPING_MAKE_DURATION_MIN,
                                   make_duration_max=self.FAST_TYPING_MAKE_DURATION_MAX,
                                   delay_min=self.FAST_TYPING_DELAY_MIN,
                                   delay_max=self.FAST_TYPING_DELAY_MAX)

        self.testCaseChecked("FUNC_TYPG_0005")
    # end def test_fast_typing_by_key_id_long_version

    @features('Keyboard')
    @features('EvtTyping')
    @level('Time-consuming')
    @services('KeyMatrix')
    def test_normal_typing_by_key_id_long_version(self):
        """
        FWQA "normal typing" test

        typing scheme = random
        Total number of keys = 40000 (EVT) or 30 (CI)
        key count = 10
        loop = 4000 (EVT) or 3 (CI)
        typing period = 1200 ms
        random typing period = 2000 ms
        make duration = 125 ms
        random make period = 90 ms
        """
        self.SHEET_CELL_ID = EvtTypingConfig.CellRange.NORMAL_TYPING_KEY
        self.RANDOM_KEY_LIST = True

        self.check_key_by_hid_code(rep_key_count=self.NORMAL_TYPING_KEY_COUNT,
                                   loop_count=self.NORMAL_TYPING_LOOPS,
                                   make_duration_min=self.NORMAL_TYPING_MAKE_DURATION_MIN,
                                   make_duration_max=self.NORMAL_TYPING_MAKE_DURATION_MIN,
                                   delay_min=self.NORMAL_TYPING_DELAY_MIN,
                                   delay_max=self.NORMAL_TYPING_DELAY_MAX)

        self.testCaseChecked("FUNC_TYPG_0006")
    # end def test_normal_typing_by_key_id_long_version
# end class TypingFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
