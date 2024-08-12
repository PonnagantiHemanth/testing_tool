#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.gtechkeymatrixemulator
:brief: Kosmos GTECH KeyMatrix Emulator Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/03/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from sys import stdout
from typing import Type

from pylibrary.emulator.keybaordlayout import AnalogKeyMatrix
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.keyboardemulator import KeyState
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulatorMixin
from pyraspi.services.kosmos.module.kbdgtech import KBD_GTECH_EMU_MODE
from pyraspi.services.kosmos.module.kbdgtech import KBD_GTECH_FUNC_MODE
from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_UPDATE
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_UPDATE_SEND
from pyraspi.services.kosmos.protocol.generated.messages import kbd_entry_t

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

GTECH_KEY_RELEASE_LEVEL = 0
GTECH_KEY_PRESS_LEVEL = 40


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosGtechKeyMatrixEmulator(KosmosKeyMatrixEmulatorMixin):
    """
    Kosmos Gtech-based KeyMatrix emulator.
    This class controls the FPGA emulator, generating the SPI traffic between the Gtech & Logitech chips.
    It emulates the Analog Switches displacement levels.

    This class does not cover the emulation of the additional Galvanic Keymatrix present in Galvatron DUT.
    For this matter, please refer to the overlying class ``KosmosDualKeyMatrixEmulator``.

    Refer to the System Level Specification document:
      Galvatron Analog Keyboard Kosmos Emulator Project
      https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc
    """

    # Update type hints
    kbd: KbdGtechModule
    keyboard_layout: Type[AnalogKeyMatrix]

    def __init__(self, kosmos, fw_id, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: Invalid Keyboard layout
        """
        super().__init__(kosmos=kosmos, fw_id=fw_id, verbose=verbose, kbd=kosmos.dt.kbd_gtech)

        assert issubclass(self.keyboard_layout, AnalogKeyMatrix), self.keyboard_layout
        assert self.keyboard_layout.IS_ANALOG, f"{fw_id} is an Analog Keyboard"
        assert not self.keyboard_layout.IS_HYBRID, f"{fw_id} is not an Hybrid Keyboard"
        assert self.keyboard_layout.KEYID_2_CHAINID, self.keyboard_layout.KEYID_2_CHAINID
    # end def __init__

    def setup_defaults(self):
        """
        Set defaults for Kosmos Gtech Emulator.
        Clear keymatrix local and remote caches and memories.
        Reset `Emulator` and `Functional` modes.

        Refer to ``KosmosKeyMatrixEmulatorMixin.setup_defaults``
        """
        super().setup_defaults()

        # 1) Reset KBD Emulator mode to REAL (emulator is offline).
        # 2) Reset KBD memories while emulator is offline. This does not require an operational DUT at this stage.
        # 3) Set KBD Functional mode to LEGACY, by default. User can change it later to ANALOG.
        # 4) Set KBD Emulator mode to EMULATED (emulator is online).
        self.kbd.emu_mode_msg(KBD_GTECH_EMU_MODE.REAL)
        self.release_all()
        self.kbd.func_mode_legacy()
        self.kbd.emu_mode_msg(KBD_GTECH_EMU_MODE.EMULATED)
    # end def setup_defaults

    def get_bank_lane_addr(self, key_id):
        # See ``KosmosKeyMatrixEmulatorMixin.get_bank_lane_addr``
        chain_id = self.keyboard_layout.KEYID_2_CHAINID[key_id]

        bank_count = self.kbd.settings.kbd_bank_count
        lane_count = self.kbd.settings.kbd_lane_count
        addr_count = self.kbd.settings.kbd_addr_count

        assert 0 <= chain_id < (bank_count * addr_count), \
            f'{key_id!r}: chain_id={chain_id} is out of bounds [0, {bank_count * addr_count - 1}].'

        if self.kbd.func_mode == KBD_GTECH_FUNC_MODE.LEGACY:
            # KBD functional mode: Legacy (Key Press & Key Release ony)
            # The mapping {chain_id} to {bank, lane, addr} is specified in the following spreadsheet, 1st tab:
            # https://docs.google.com/spreadsheets/d/1U3Ee_pG--NqNQnPZv2F81-B8Tf07ubyUvebCBd-INdU/view#gid=1150794709
            bank = (chain_id // (lane_count // 2)) & 1
            lane = chain_id % (lane_count // 2)
            addr = chain_id // lane_count

        elif self.kbd.func_mode == KBD_GTECH_FUNC_MODE.ANALOG:
            # KBD functional mode: Analog (0-40 displacement levels)
            # The mapping {chain_id} to {bank, lane, addr} is specified in the following spreadsheet, 2nd tab:
            # https://docs.google.com/spreadsheets/d/1U3Ee_pG--NqNQnPZv2F81-B8Tf07ubyUvebCBd-INdU/view#gid=2084639238
            bank = chain_id & 1
            lane = 0x00  # irrelevant here; displacement value will be used instead
            addr = chain_id >> 1
        else:
            raise ValueError(self.kbd.func_mode)
        # end if

        assert 0 <= bank < bank_count, f'{key_id!r}: bank={bank} is out of bounds [0, {bank_count - 1}]'
        assert 0 <= lane < lane_count // 2, f'{key_id!r}: lane={lane} is out of bounds [0, {lane_count // 2 - 1}]'
        assert 0 <= addr < addr_count, f'{key_id!r}: addr={addr} is out of bounds  [0, {addr_count - 1}]'

        return bank, lane, addr
    # end def get_bank_lane_addr

    def _set_key_state_debug_print(self, key_id, state):
        # See ``KosmosKeyMatrixEmulatorMixin._set_key_state_debug_print``
        bank, lane, addr = self.get_bank_lane_addr(key_id)
        lanes = self._compute_new_lanes_state(bank=bank, addr=addr, lane=lane, state=state)
        chain_id = self.keyboard_layout.KEYID_2_CHAINID[key_id]

        stdout.write(f'  {state.name:5s} {KEY_ID(key_id).name}: chain_id={chain_id:#04x}, '
                     f'bank={bank}, addr={addr}, lane={lane}, lanes={lanes:#04x}\n')
    # end def _set_key_state_debug_print

    def _compute_new_lanes_state(self, bank, addr, lane, state):
        # See ``KosmosKeyMatrixEmulatorMixin._compute_new_lanes_state``
        if self.kbd.func_mode == KBD_GTECH_FUNC_MODE.LEGACY:
            # KBD functional mode: Legacy (Key Press & Key Release ony)
            return super()._compute_new_lanes_state(bank=bank, addr=addr, lane=lane, state=state)
        elif self.kbd.func_mode == KBD_GTECH_FUNC_MODE.ANALOG:
            # KBD functional mode: Analog (Key Release: displacement level 0 / Key Press displacement level 40)
            return GTECH_KEY_RELEASE_LEVEL if state == KeyState.BREAK else GTECH_KEY_PRESS_LEVEL
        else:
            raise ValueError(self.kbd.func_mode)
        # end if
    # end def _compute_new_lanes_state

    def key_displacement(self, key_id, displacement, immediate_execution=True, update_only=False):
        """
        Emulate Analog Key displacement.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID`` or ``int``
        :param displacement: Key displacement in millimetre, from 0 (Released) to 40 (Pressed).
        :type displacement: ``int``
        :param immediate_execution: Flag enabling to insertion of an execute instruction - OPTIONAL
        :type immediate_execution: ``bool``
        :param update_only: Flag enabling to only load the switch state of a given key into the keyboard state RAM and
                            not transfer it to the switching hardware - OPTIONAL
        :type update_only: ``bool``

        :raise ``AssertionError``: Out-of-bounds displacement value
        """
        assert GTECH_KEY_RELEASE_LEVEL <= displacement <= GTECH_KEY_PRESS_LEVEL, (
            f'[{key_id!r}] displacement={displacement} is out-of-bounds '
            f'[{GTECH_KEY_RELEASE_LEVEL}, {GTECH_KEY_PRESS_LEVEL}]')

        bank, lane, addr = self.get_bank_lane_addr(key_id)
        lanes = displacement

        # Send lanes update
        if lanes != self.memory_cache[bank][addr]:
            # Debug print
            if self.verbose:
                chain_id = self.keyboard_layout.KEYID_2_CHAINID[key_id]
                stdout.write(f'  {KEY_ID(key_id).name}: displacement={displacement:02}, chain_id={chain_id:#04x}, '
                             f'bank={bank}, addr={addr}, lane={lane}, lanes={lanes:#04x}\n')
            # end if

            # Update local memory cache
            self.memory_cache[bank][addr] = lanes

            # Prepare register Update (& Send) command to KBD controller
            kbd_entry = kbd_entry_t()
            kbd_entry.bit.lane = lanes
            kbd_entry.bit.addr = addr
            kbd_entry.bit.bank = bank
            kbd_entry.bit.command = KBD_COMMAND_UPDATE if update_only else KBD_COMMAND_UPDATE_SEND

            # Add KBD instruction to buffer
            self.kbd.append(kbd_entry)

            if immediate_execution:
                # Create an EXECUTE instruction to trigger the event
                self._kosmos.pes.execute(action=self.kbd.action_event.SEND)

                # Add an instruction to wait until the end of previous KBD event
                self.kbd.pes_wait_kbd()
            # end if
        # end if

        # Start to play the defined scenario
        self._kosmos.sequencer.play_sequence()
    # end def key_displacement
# end class KosmosGtechKeyMatrixEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
