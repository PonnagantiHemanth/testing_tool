#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.keyboard.ghostkeys.robustness
:brief: Hid Keyboard ghost keys robustness test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/06/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from itertools import permutations
from random import sample

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hid.keyboard.ghostkeys.ghostkeys import GhostKeysTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class GhostKeysRobustnessTestCase(GhostKeysTestCase):
    """
    Validate Keyboard Ghost Keys robustness TestCases
    """

    @features('Keyboard')
    @features('GhostKeys')
    @level('Robustness')
    @services('KeyMatrix')
    def test_ghost_key_permutations(self):
        """
        Check some permutations of 4 keys triggering double ghost keys situations.
        """
        self.kosmos.sequencer.offline_mode = True

        for base_index in range(KbdMatrix.COL_15):
            keys = KeyMatrixTestUtils.get_key_on_square(self, row_indexes=(1, 2),
                                                        column_indexes=(base_index, base_index+1))
            if keys is not None:
                break
            # end if
            assert base_index < KbdMatrix.COL_15 - 1, 'No Ghost keys use case found with the current key matrix ' \
                                                      'definition !'
        # end for
        # this will create all permutations of length 4 of keys
        key_quadruplets = list(permutations(keys))

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key presses on the quadruplet {str(key_quadruplet[0])} & '
                                     f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_quadruplet,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key releases on the quadruplet {str(key_quadruplet[0])} & '
                                     f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_quadruplet,
                                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(timeout=60, block=True)

        for key_quadruplet in key_quadruplets:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the HID reports related to the presses on {str(key_quadruplet[0])} & '
                                      f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                LogHelper.log_info(self, f'Press {str(key_quadruplet[index])}')
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], MAKE))
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the HID reports related to the releases on {str(key_quadruplet[0])} & '
                                      f'{str(key_quadruplet[1])} & {str(key_quadruplet[2])} & {str(key_quadruplet[3])}')
            # ----------------------------------------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                LogHelper.log_info(self, f'Release {str(key_quadruplet[index])}')
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("ROB_GHOST_0001")
    # end def test_ghost_key_permutations

    @features('Keyboard')
    @features('GhostKeys')
    @level('Robustness')
    @services('KeyMatrix')
    def test_keys_on_square_all_rows(self):
        """
        Check some combination of 4 keys triggering double ghost keys situations.
        """
        self.kosmos.sequencer.offline_mode = True
        last_key_id = list(self.button_stimuli_emulator.get_key_id_list())[-1]
        last_key_row_index, _ = self.button_stimuli_emulator.get_row_col_indexes(key_id=last_key_id)

        key_quadruplets = []
        for row_index in range(last_key_row_index):
            keys = KeyMatrixTestUtils.get_key_on_square(
                self, row_indexes=(row_index, row_index+1), column_indexes=(1, 2))
            if keys is not None:
                key_quadruplets.append(keys)
            # end if
        # end if

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key presses on the quadruplet {key_quadruplet[0]} & '
                                     f'{key_quadruplet[1]} & {key_quadruplet[2]} & {key_quadruplet[3]}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_quadruplet,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key releases on the quadruplet {key_quadruplet[0]} & '
                                     f'{key_quadruplet[1]} & {key_quadruplet[2]} & {key_quadruplet[3]}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_quadruplet,
                                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(timeout=60, block=True)

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the HID reports with 4 keys pressed simultaneously')
            # ---------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], MAKE))
            # end for

            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("ROB_GHOST_0002")
    # end def test_keys_on_square_all_rows

    @features('Keyboard')
    @features('GhostKeys')
    @level('Robustness')
    @services('KeyMatrix')
    def test_keys_on_square_all_columns(self):
        """
        Check some combination of 4 keys triggering double ghost keys situations.
        """
        self.kosmos.sequencer.offline_mode = True
        last_key_id = list(self.button_stimuli_emulator.get_key_id_list())[-1]
        _, last_key_col_index = self.button_stimuli_emulator.get_row_col_indexes(key_id=last_key_id)

        key_quadruplets = []
        for col_index in range(last_key_col_index):
            keys = KeyMatrixTestUtils.get_key_on_square(
                self, row_indexes=(1, 2), column_indexes=(col_index, col_index+1))
            if keys is not None:
                key_quadruplets.append(keys)
            # end if
        # end if

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key presses on the quadruplet {key_quadruplet[0]} & '
                                     f'{key_quadruplet[1]} & {key_quadruplet[2]} & {key_quadruplet[3]}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_quadruplet,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key releases on the quadruplet {key_quadruplet[0]} & '
                                     f'{key_quadruplet[1]} & {key_quadruplet[2]} & {key_quadruplet[3]}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_quadruplet,
                                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(timeout=60, block=True)

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the HID reports with 4 keys pressed simultaneously')
            # ---------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], MAKE))
            # end for

            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("ROB_GHOST_0003")
    # end def test_keys_on_square_all_columns

    @features('Keyboard')
    @features('GhostKeys')
    @level('Robustness')
    @services('KeyMatrix')
    def test_keys_on_square_randomly(self):
        """
        Check some combination of 4 keys triggering double ghost keys situations.
        """
        self.kosmos.sequencer.offline_mode = True
        last_key_id = list(self.button_stimuli_emulator.get_key_id_list())[-1]
        last_key_row_index, last_key_col_index = self.button_stimuli_emulator.get_row_col_indexes(key_id=last_key_id)

        key_quadruplets = []
        for _ in range(4):
            row_index_list = sample(range(last_key_row_index), 2)
            col_index_list = sample(range(last_key_col_index), 2)
            keys = KeyMatrixTestUtils.get_key_on_square(
                self, row_indexes=(row_index_list[0], row_index_list[1]),
                column_indexes=(col_index_list[0], col_index_list[1]))
            if keys is not None:
                key_quadruplets.append(keys)
            # end if
        # end if

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key presses on the quadruplet {key_quadruplet[0]} & '
                                     f'{key_quadruplet[1]} & {key_quadruplet[2]} & {key_quadruplet[3]}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_quadruplet,
                                                             delay=ButtonStimuliInterface.DEFAULT_DURATION)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate key releases on the quadruplet {key_quadruplet[0]} & '
                                     f'{key_quadruplet[1]} & {key_quadruplet[2]} & {key_quadruplet[3]}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_quadruplet,
                                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(timeout=60, block=True)

        for key_quadruplet in key_quadruplets:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the HID reports with 4 keys pressed simultaneously')
            # ---------------------------------------------------------------------------
            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], MAKE))
            # end for

            for index in range(len(key_quadruplet)):
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                              key=KeyMatrixTestUtils.Key(key_quadruplet[index], BREAK))
            # end for
        # end for

        self.testCaseChecked("ROB_GHOST_0004")
    # end def test_keys_on_square_randomly

# end class GhostKeysRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
