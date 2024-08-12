#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.typing.typing
:brief: Hid Keyboard Typing test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/04/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import datetime
import time
import random
from random import randint

from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TypingTestCase(BaseTestCase):
    """
    Validate Keyboard Typing requirements.
    """

    # Refer this sheet link for parameter details (all definitions are in ms)
    # https://docs.google.com/spreadsheets/d/1FQowBsPKx5KUQy0uDrDUs879969GCmQ6/view?gid=1713721740#gid=1713721740

    # Refer this sheet link for typing test template
    # https://docs.google.com/spreadsheets/d/1FQowBsPKx5KUQy0uDrDUs879969GCmQ6/view?gid=835542216#gid=835542216

    DEFAULT_KEY_COUNT = 10

    # ENDURANCE
    ENDURANCE_TYPING_LOOPS = None
    ENDURANCE_TYPING_KEY_COUNT = DEFAULT_KEY_COUNT
    ENDURANCE_TYPING_MAKE_DURATION_MIN = 40
    ENDURANCE_TYPING_MAKE_DURATION_MAX = 80
    ENDURANCE_TYPING_DELAY_MIN = 25
    ENDURANCE_TYPING_DELAY_MAX = 120

    # FAST_TYPING
    FAST_TYPING_LOOPS = None
    FAST_TYPING_KEY_COUNT = DEFAULT_KEY_COUNT
    FAST_TYPING_MAKE_DURATION_MIN = 12
    FAST_TYPING_MAKE_DURATION_MAX = 20
    FAST_TYPING_DELAY_MIN = 32
    FAST_TYPING_DELAY_MAX = 44

    # GAMING
    GAMING_LOOPS = None
    GAMING_KEY_COUNT = DEFAULT_KEY_COUNT
    GAMING_TYPING_MAKE_DURATION_MIN = 300
    GAMING_TYPING_MAKE_DURATION_MAX = 300
    GAMING_TYPING_NEXT_MAKE_DURATION_MIN = 100
    GAMING_TYPING_NEXT_MAKE_DURATION_MAX = 200

    # WAKE UP QUICK
    WAKE_UP_QUICK_LOOPS = None
    WAKE_UP_QUICK_KEY_COUNT = DEFAULT_KEY_COUNT
    WAKE_UP_QUICK_TYPING_MAKE_DURATION_MIN = 80
    WAKE_UP_QUICK_TYPING_MAKE_DURATION_MAX = 80
    WAKE_UP_QUICK_TYPING_DELAY_MIN = 920
    WAKE_UP_QUICK_TYPING_DELAY_MAX = 920
    WAKE_UP_QUICK_TYPING_SWEEP_MIN = 40
    WAKE_UP_QUICK_TYPING_SWEEP_MAX = 1000
    WAKE_UP_QUICK_TYPING_SWEEP_DEC = -1

    # WAKE UP SLOW
    WAKE_UP_SLOW_LOOPS = None
    WAKE_UP_SLOW_KEY_COUNT = DEFAULT_KEY_COUNT
    WAKE_UP_SLOW_TYPING_MAKE_DURATION_MIN = 80
    WAKE_UP_SLOW_TYPING_MAKE_DURATION_MAX = 80
    WAKE_UP_SLOW_TYPING_DELAY_MIN = 2920
    WAKE_UP_SLOW_TYPING_DELAY_MAX = 2920
    WAKE_UP_SLOW_TYPING_SWEEP_MIN = 1000
    WAKE_UP_SLOW_TYPING_SWEEP_MAX = 3000
    WAKE_UP_SLOW_TYPING_SWEEP_DEC = -10

    # NORMAL TYPING
    NORMAL_TYPING_LOOPS = None
    NORMAL_TYPING_KEY_COUNT = DEFAULT_KEY_COUNT
    NORMAL_TYPING_MAKE_DURATION_MIN = 80
    NORMAL_TYPING_MAKE_DURATION_MAX = 170
    NORMAL_TYPING_DELAY_MIN = 120
    NORMAL_TYPING_DELAY_MAX = 2030

    def setUp(self):
        """
        Handle test prerequisites.
        """

        super().setUp()

        self.THOUSAND_MILLI_SEC = 1000
        self.KEY_COUNT = 0
        self.SHEET_CELL_ID = None
        self.SWEEP_MIN = None
        self.SWEEP_MAX = None
        self.SWEEP_DEC = None
        self.RANDOM_KEY_LIST = False

        self.config = self.f.PRODUCT.DEVICE.EVT_AUTOMATION.TYPING_TEST

        if not self.config.F_RunTypingTestCompleteEVT:
            self.WAKE_UP_QUICK_LOOPS = 3
            self.WAKE_UP_SLOW_LOOPS = 2
            self.GAMING_LOOPS = 3
            self.NORMAL_TYPING_LOOPS = 3
            self.FAST_TYPING_LOOPS = 10
            self.ENDURANCE_TYPING_LOOPS = 10
        else:
            self.WAKE_UP_QUICK_LOOPS = 100
            self.WAKE_UP_SLOW_LOOPS = 20
            self.GAMING_LOOPS = 200
            self.NORMAL_TYPING_LOOPS = 4000
            self.FAST_TYPING_LOOPS = 10000
            self.ENDURANCE_TYPING_LOOPS = 30000
        # end if

        if self.config.F_CreateGoogleSheet:
            from pytestbox.tools.reportgenerator.google_sheet_access import GoogleSheetReport
            self.google_sheet_report = GoogleSheetReport(self)
        # end if

        self.get_list = None
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # Be sure the full sequence was executed before quiting
            self.kosmos.sequencer.wait_end_of_sequence()
        # end with

        if self.get_list is not None and self.config.F_CreateGoogleSheet:
            self.google_sheet_report.write_sheet(value=self.get_list, cell_range=self.SHEET_CELL_ID)
        # end if

        super().tearDown()
    # end def tearDown

    def build_key_list_adaptive_period(self, make_duration_min, make_duration_max, delay_min, delay_max,
                                       random_keys_count):
        """
        Build a list of several random keys to be pressed.

        :param make_duration_min: Timing in ms for make minimum duration
        :type make_duration_min: ``int``
        :param make_duration_max: Timing in ms for make maximum duration
        :type make_duration_max: ``int``
        :param delay_min: delay minimum in ms for gap between break and next make
        :type delay_min: ``int``
        :param delay_max: delay maximum in ms for gap between break and next make
        :type delay_max: ``int``
        :param random_keys_count: Number of randomly chosen key to insert in the list
        :type random_keys_count: ``int``

        :return: The list of key id
        :rtype: ``list``
        """
        self.kosmos.sequencer.offline_mode = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Build a list of {random_keys_count} keys to be pressed')
        # --------------------------------------------------------------------------------------------------------------
        keys = KeyMatrixTestUtils.get_key_list(
            self, group_count=random_keys_count, group_size=1, random=False,
            excluded_keys=[KEY_ID.FN_KEY, KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3, KEY_ID.FN_LOCK,
                           KEY_ID.KEYBOARD_MUTE, KEY_ID.SCREEN_CAPTURE])
        if self.RANDOM_KEY_LIST:
            random.shuffle(keys)
        # end if

        for (key_id,) in keys:
            # Random Make duration
            make_duration = (randint(make_duration_min, make_duration_max) / self.THOUSAND_MILLI_SEC)
            if self.SWEEP_MIN is not None and self.SWEEP_MAX is not None and self.SWEEP_DEC is not None:
                self.temp_sweep_max -= abs(self.SWEEP_DEC)

                if self.temp_sweep_max < self.SWEEP_MIN:
                    self.temp_sweep_max = self.SWEEP_MAX
                # end if
                make_duration = self.temp_sweep_max / self.THOUSAND_MILLI_SEC
            # end if

            # Random Typing period = make duration + delay
            delay = (randint(delay_min, delay_max) / self.THOUSAND_MILLI_SEC)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the key with id={str(key_id)} with a '
                                     f'duration of {make_duration} and a delay of {delay}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=make_duration, repeat=1, delay=delay)
        # end for

        self.kosmos.sequencer.offline_mode = False
        return keys

    # end def build_key_list_adaptive_period

    def check_key_by_hid_code(self, rep_key_count, loop_count, make_duration_min, make_duration_max, delay_min,
                              delay_max, sleep=False):
        """
        Execute Key Press and check HID code.

        :param rep_key_count: The number of keys pressed in a kosmos sequence
        :type rep_key_count: ``int``
        :param loop_count: number of repetitions of the kosmos sequence
        :type loop_count: ``int``
        :param make_duration_min: Timing in ms for make minimum duration
        :type make_duration_min: ``int``
        :param make_duration_max: Timing in ms for make maximum duration
        :type make_duration_max: ``int``
        :param delay_min: delay minimum in ms for gap between break and next make
        :type delay_min: ``int``
        :param delay_max: delay maximum in ms for gap between break and next make
        :type delay_max: ``int``
        :param sleep: Flag indicating that the DUT is forced to deep sleep before executing the kosmos sequence
        :type sleep: ``bool``
        """
        self.temp_sweep_max = self.SWEEP_MAX
        start_time = time.time()
        for loop in range(loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Loop Count = {loop}')
            # ----------------------------------------------------------------------------------------------------------
            if sleep is True:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Force DUT in deep sleep by sending SetPowerMode with powerModeNumber = 3')
                # ------------------------------------------------------------------------------------------------------
                PowerModesTestUtils.HIDppHelper.enter_deep_sleep(self)
            # end if

            key_id_list = self.build_key_list_adaptive_period(make_duration_min=make_duration_min,
                                                              make_duration_max=make_duration_max,
                                                              delay_min=delay_min, delay_max=delay_max,
                                                              random_keys_count=rep_key_count)

            # Upload the complete scenario into the Kosmos
            self.kosmos.sequencer.play_sequence(timeout=60)
            for (key_id,) in key_id_list:
                self.KEY_COUNT = self.KEY_COUNT + 1
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard report on key {str(key_id)}')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
            # end for

            end_time = time.time()
            self.get_list = [[self.KEY_COUNT, loop + 1, rep_key_count,
                              str(make_duration_min), str(make_duration_max),
                              str(delay_min), str(delay_max),
                              str(datetime.timedelta(seconds=end_time - start_time))]]
        # end for
    # end def check_key_by_hid_code

    def check_gaming_key_by_hid_code(self, rep_key_count, loop_count, make_duration_min, make_duration_max,
                                     next_make_at_min, next_make_at_max):
        """
        Execute Key Press and check HID code.

        :param rep_key_count: The number of keys pressed in a kosmos sequence
        :type rep_key_count: ``int``
        :param loop_count: number of repetitions of the kosmos sequence
        :type loop_count: ``int``
        :param make_duration_min: Timing in ms for make minimum duration
        :type make_duration_min: ``int``
        :param make_duration_max: Timing in ms for make maximum duration
        :type make_duration_max: ``int``
        :param next_make_at_min: next make minimum in ms trigger the next make
        :type next_make_at_min: ``int``
        :param next_make_at_max: next make maximum in ms trigger the next make
        :type next_make_at_max: ``int``
        """
        start_time = time.time()
        for loop in range(loop_count):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Loop Count = {loop}')
            # ----------------------------------------------------------------------------------------------------------

            keys = KeyMatrixTestUtils.get_key_list(
                self, group_count=rep_key_count, group_size=1, random=False,
                excluded_keys=[KEY_ID.FN_KEY, KEY_ID.HOST_1, KEY_ID.HOST_2, KEY_ID.HOST_3, KEY_ID.FN_LOCK,
                               KEY_ID.KEYBOARD_MUTE, KEY_ID.SCREEN_CAPTURE])

            make_duration = (randint(make_duration_min, make_duration_max) / self.THOUSAND_MILLI_SEC)
            next_make = (randint(next_make_at_min, next_make_at_max) / self.THOUSAND_MILLI_SEC)

            for keyID_index in range(len(keys)):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate a keystroke on the key with id={str(keyID_index)} with a '
                                         f'duration of {make_duration} and next make at {next_make}')
                # ------------------------------------------------------------------------------------------------------
                self.KEY_COUNT = self.KEY_COUNT + 1
                if keyID_index < 2:
                    self.make_and_break(key_id=[keys[keyID_index][0]], state=[MAKE],
                                        time_interval=next_make)
                else:
                    self.make_and_break(key_id=[keys[keyID_index][0], keys[keyID_index-2][0]], state=[MAKE, BREAK],
                                        time_interval=next_make)
                # end if
                if keyID_index == len(keys)-1:
                    self.make_and_break(key_id=[keys[keyID_index][0], keys[keyID_index-1][0]],
                                        state=[BREAK, BREAK], time_interval=next_make)
                # end if
            # end for

            end_time = time.time()
            self.get_list = [[self.KEY_COUNT, loop + 1, rep_key_count,
                              str(make_duration_min), str(make_duration_max),
                              str(next_make_at_min), str(next_make_at_max),
                              str(datetime.timedelta(seconds=end_time - start_time))]]
        # end for
    # end def check_gaming_key_by_hid_code

    def make_and_break(self, key_id, state, time_interval):
        start_time = time.time()

        for key_index, state_index in enumerate(range(len(key_id))):
            if state[state_index] is MAKE:
                self.button_stimuli_emulator.key_press(key_id=key_id[key_index])
            else:
                self.button_stimuli_emulator.key_release(key_id=key_id[key_index])
            # end if
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_id[key_index],
                                                                                     state[state_index]))
        # end for
        while (time.time() - start_time) < time_interval:
            continue
        # end while
    # end def make_and_break
# end class TypingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
