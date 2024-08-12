#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.hybridkeymatrixemulator
:brief: Kosmos HybridKeyMatrix Emulator Class
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2023/03/06
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from typing import Type

from pylibrary.emulator.keybaordlayout import HybridKeyMatrix
from pyraspi.services.keyboardemulator import KeyState
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosHybridKeyMatrixEmulator(KosmosKeyMatrixEmulator):
    """
    KeyMatrix emulator leveraging Kosmos test instrument (i.e. granddaughter board)
    This implementation is specific for Hybrid (optical + galvanic) switches keyboard

    Refer to the System Level Specification document
      KEYBOARD MATRIX CONTROLLER IP MODULE II
      https://docs.google.com/document/d/1yRsmBT0WLcmUFKmsOk50_oxwRLvlRtWfJDsCTSFPhZY
    """

    # Update type hint
    keyboard_layout: Type[HybridKeyMatrix]

    def __init__(self, kosmos, fw_id, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: multiple source of error:
         - Invalid fw_id
         - ``AssertionError``: Invalid keyboard_layout
        """
        super().__init__(kosmos=kosmos, fw_id=fw_id, verbose=verbose)
        assert self._keyboard_layout.IS_HYBRID, f"{fw_id} is not an Hybrid Keyboard"
        assert issubclass(self.keyboard_layout, HybridKeyMatrix), self.keyboard_layout
    # end def __init__

    def _init_default_memory_cache(self):
        """
        Initialize the default memory cache of a hybrid matrix.

        All the switches corresponding to optical elements should receive a "MAKE"
        The standard galvanic switches and the control/feedback signals are left alone
        """
        super()._init_default_memory_cache()
        self._init_memory_cache()

        for key_id in self._keyboard_layout.REVERSE_MAKE_LOGIC_KEYS:
            bank, lane, addr = self.get_bank_lane_addr(key_id)
            # Compute new lanes state
            lanes = self._compute_new_lanes_state(bank=bank, addr=addr, lane=lane, state=KeyState.MAKE)

            # Update local default memory cache
            self.default_memory_cache[bank][addr] = lanes
        # end for
    # end def _init_default_memory_cache

    def _set_key_state(self, key_id, state, immediate_execution=True, update_only=False):
        """
        Change the switch state of a given key, based on its row & col indexes.
        For the Hybrid keyboard, it is needed to check if the target key switch is optical.
        If that is the case, the MAKE and BREAK instructions are inverted.

        Refer to the System Level Specification document referenced in the description of the class.

        :param key_id: The target key
        :type key_id: ``KEY_ID``
        :param state: BREAK (off, released) or MAKE (on, pressed)
        :type state: ``KeyState``
        :param immediate_execution: Flag enabling to insertion of an execute instruction - OPTIONAL
        :type immediate_execution: ``bool``
        :param update_only: Flag enabling to only load the switch state of a given key into the keyboard state RAM and
                            not transfer it to the switching hardware - OPTIONAL
        :type update_only: ``bool``
        """
        if key_id in self._keyboard_layout.REVERSE_MAKE_LOGIC_KEYS:
            key_state = KeyState.MAKE if state == KeyState.BREAK else KeyState.BREAK
        else:
            key_state = state
        # end if
        super()._set_key_state(key_id=key_id, state=key_state, immediate_execution=immediate_execution,
                                   update_only=update_only)
    # end def _set_key_state
# end class KosmosHybridKeyMatrixEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
