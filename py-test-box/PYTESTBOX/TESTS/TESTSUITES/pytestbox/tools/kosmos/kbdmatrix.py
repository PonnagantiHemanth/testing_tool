#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.kosmos.kbdmatrix
:brief: Keyboard Matrix Emulator Validation
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/12/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pyraspi.services.keyboardemulator import KeyState
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.tools.kosmos.kosmos import KosmosTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KosmosKbdMatrixTestCase(KosmosTestCase):
    """
    Kosmos Keymatrix Emulator Unit Test Validation

    NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY PRODUCT SPECIFICATIONS.
    """
    def set_default_memory_cache(self, key_ids_pressed):
        """
        Set to the default memory cache some pressed keys containing in  ``key_ids_pressed``. After
        calling ``send_default_memory_cache_to_fpga`` and ``release_all`` method, this list of keys will be pressed
        by default

        :param key_ids_pressed: List of unique identifier of the keys to emulate a press
        :type key_ids_pressed: ``List[KEY_ID]``
        """
        self.button_stimuli_emulator._init_default_memory_cache()
        for key_id in key_ids_pressed:
            bank, lane, addr = self.button_stimuli_emulator.get_bank_lane_addr(key_id)
            state = KeyState.MAKE
            # For the Hybrid keyboard, it is needed to check if the target key switch is optical.
            # If that is the case, the MAKE and BREAK instructions are inverted.
            if (self.button_stimuli_emulator._keyboard_layout.IS_HYBRID and
                    key_id in self.button_stimuli_emulator._keyboard_layout.REVERSE_MAKE_LOGIC_KEYS):
                state = KeyState.BREAK
            # end if

            # Compute new lanes state
            lanes = self.button_stimuli_emulator._compute_new_lanes_state(bank=bank, addr=addr, lane=lane, state=state)
            # Update local default memory cache
            self.button_stimuli_emulator.default_memory_cache[bank][addr] = lanes
        # end for
    # end def set_default_memory_cache

    @features('Keyboard')
    @level('Tools')
    @services('KeyMatrix')
    def test_default_memory_cache_on_all_available_keys(self):
        """
        Check if all key matrix switches (one by one) can be closed when calling
        'self.button_stimuli_emulator.release_all()'
        """
        self.post_requisite_clean_default_memory_cache = True
        keys = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=1, random=False)
        for (key_id,) in keys:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send default memory cache to fpga with {key_id!s} pressed')
            # ----------------------------------------------------------------------------------------------------------
            self.set_default_memory_cache(key_ids_pressed=[key_id])
            self.button_stimuli_emulator.send_default_memory_cache_to_fpga()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Reset the keymatrix with the default memory cache')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.release_all()
            sleep(ButtonStimuliInterface.DEFAULT_DURATION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the key {key_id!s}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send default memory cache to fpga with all keys released')
            # ----------------------------------------------------------------------------------------------------------
            self.set_default_memory_cache(key_ids_pressed=[])
            self.button_stimuli_emulator.send_default_memory_cache_to_fpga()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Reset the keymatrix with the default memory cache')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.release_all()
            sleep(ButtonStimuliInterface.DEFAULT_DURATION)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the key {key_id!s}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for
    # end def test_default_memory_cache_on_all_available_keys
# end class KosmosKbdMatrixTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
