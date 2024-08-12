#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.keymatrixemulator
:brief: Kosmos KeyMatrix Emulator Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import abstractmethod
from copy import deepcopy
from sys import stdout
from typing import Type
from typing import Union

from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.daemon import Daemon
from pyraspi.services.keyboardemulator import KeyState
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
from pyraspi.services.kosmos.module.kbdmatrix import KbdMatrixModule
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_RESET
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_SEND
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_UPDATE
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_UPDATE_SEND
from pyraspi.services.kosmos.protocol.generated.messages import kbd_entry_t

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# Workaround delay in order to be sure the PES FIFO can be filled faster than the instructions are consumed.
# This value was found empirically by analyzing the PES FIFO counter
DELAY_S_BETWEEN_KBD_COMMAND_UPDATE = 4e-6  # 4us converted in second

# Post release_all delay: Wait until the product/platform can detect the release
# 50ms is a conservative value, it should always be greater than 100PercentBreakDebounceUs parameter from the
# product settings file
DELAY_S_POST_RELEASE_ALL = 50e-3  # in second

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosKeyMatrixEmulatorMixin(KeyboardMixin):
    """
    Mixin class for Kosmos KeyMatrix emulators.
    """

    # Define local memory caches; those reflect the FPGA cache memories; which reflect the DUT keymatrix state.
    memory_cache = [[]]  # format: memory_cache[BANK][ADDR]
    default_memory_cache = [[]]  # format: default_memory_cache[BANK][ADDR]

    # Set type hint
    kbd: Union[KbdMatrixModule, KbdGtechModule]

    def __init__(self, kosmos, fw_id, kbd, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param kbd: The low-level Kosmos KBD module
        :type kbd: ``KbdMatrixModule or KbdGtechModule``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: multiple source of error:
         - If instantiated on non-Kosmos hardware
         - Invalid `kbd` type
        """
        assert Daemon.is_host_kosmos(), 'This class supports only Kosmos hardware'

        super().__init__(fw_id=fw_id, verbose=verbose)

        assert isinstance(kbd, (KbdMatrixModule, KbdGtechModule)), kbd

        self._kosmos = kosmos
        self.kbd = kbd

        # Compute lane mask as to fill the bit width of one bank
        self._lanes_mask = (1 << self.kbd.settings.kbd_lane_count // self.kbd.settings.kbd_bank_count) - 1

        self.setup_defaults()
    # end def __init__

    @abstractmethod
    def setup_defaults(self):
        """
        Set defaults settings
        """
        self._init_default_memory_cache()
        self._init_memory_cache()
    # end def setup_defaults

    def _init_memory_cache(self):
        """
        Init or reset the local memory cache.
        """
        self.memory_cache = deepcopy(self.default_memory_cache)
    # end def _init_memory_cache

    def _init_default_memory_cache(self):
        """
        Initialize the default memory cache
        """
        addr_count = self.kbd.settings.kbd_addr_count
        self.default_memory_cache = [[0] * addr_count, [0] * addr_count]
    # end def _init_default_memory_cache

    def _sleep(self, delay):
        # See ``KeyboardMixin._sleep``
        if delay is not None and delay > 0:
            self._kosmos.dt.pes.delay(delay_s=delay)
        # end if
    # end def _sleep

    def release_all(self, post_delay=DELAY_S_POST_RELEASE_ALL):
        # See ``ButtonStimuliInterface.release_all``
        # Refer to the System Level Specification document referenced in the description of the class.

        # Update local memory cache (clear)
        self._init_memory_cache()

        # Prepare Reset command to KBD controller
        kbd_entry = kbd_entry_t()
        kbd_entry.bit.command = KBD_COMMAND_RESET

        # Add KBD instruction to buffer
        self.kbd.append(kbd_entry)

        # Create an EXECUTE instruction to trigger the event
        self._kosmos.dt.pes.execute(action=self.kbd.action_event.SEND)

        # Add an instruction to wait until the end of previous KBD event
        self.kbd.pes_wait_kbd()

        # Eventually, wait until the product/platform can detect the release
        self._sleep(post_delay)

        # Apply the previous instructions
        self._kosmos.dt.sequencer.play_sequence(timeout=1 + post_delay)
    # end def release_all

    def change_host(self, host_index=None, delay=2):
        # See ``ButtonStimuliInterface.change_host``
        super().change_host(host_index=host_index, delay=delay)

        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def change_host

    def enter_pairing_mode(self, host_index=None, delay=2):
        # See ``ButtonStimuliInterface.enter_pairing_mode``
        super().enter_pairing_mode(host_index=host_index, delay=delay)

        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def enter_pairing_mode

    def keystroke(self, key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION, repeat=1,
                  delay=ButtonStimuliInterface.DEFAULT_DELAY):
        # See ``ButtonStimuliInterface.keystroke``
        assert key_id in self._keyboard_layout.KEYS, f'The Keyboard emulator don\'t support the key : {repr(key_id)}'
        assert duration is not None or duration == 0, f'Wrong duration parameter, got {duration}'

        if self.verbose:
            rep = f' ({repeat} times)' if repeat > 1 else ''
            stdout.write(f'keystroke: {KEY_ID(key_id).name}{rep}\n')
        # end if

        for _ in range(repeat):
            # Generate the MAKE user action
            # + Add an immediate EXECUTE instruction to trigger the make
            self._set_key_state(key_id, state=KeyState.MAKE, immediate_execution=True)

            # Create a DELAY event to manage the duration of the make and trigger the release
            self._kosmos.dt.pes.delay(delay_s=duration, action=self.kbd.action_event.SEND)

            # Generate the RELEASE user action
            self._set_key_state(key_id, state=KeyState.BREAK, immediate_execution=False)

            # Add an instruction to wait until the end of previous KBD event
            self.kbd.pes_wait_kbd()

            if delay is not None and delay > 0:
                # Create a DELAY event to prevent any other action to occur
                self._kosmos.dt.pes.delay(delay_s=delay)
            # end if

            # Start to play the defined scenario
            self._kosmos.dt.sequencer.play_sequence()
        # end for
    # end def keystroke

    def key_press(self, key_id):
        # See ``ButtonStimuliInterface.key_press``
        super().key_press(key_id=key_id)

        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def key_press

    def key_release(self, key_id):
        # See ``ButtonStimuliInterface.key_release``
        super().key_release(key_id=key_id)

        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def key_release

    def multiple_keys_press(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_press``
        if delay is not None:
            super().multiple_keys_press(key_ids=key_ids, delay=delay)
        else:
            for key_id in key_ids:
                self._set_key_state(key_id, state=KeyState.MAKE, update_only=True)
                # Workaround : When there is no other action, filling one instruction in PES FIFO takes 1.14 us
                # while the execution of KBD_COMMAND_UPDATE by kbd module take 120 ns. Moreover in this loop there
                # are 2 PES instructions and 1 KBD instruction that are linked together. So the PES FIFO empties
                # faster than it can be filled, leading to errors.
                # That's why a 4us delay is added here to be sure the PES FIFO can be filled faster than the
                # instructions are consumed. This value was found empirically by analyzing the PES FIFO counter
                self._kosmos.dt.pes.delay(delay_s=DELAY_S_BETWEEN_KBD_COMMAND_UPDATE)
            # end for

            # Prepare Send command to KBD controller
            kbd_entry = kbd_entry_t()
            kbd_entry.bit.command = KBD_COMMAND_SEND

            # Add KBD instruction to buffer
            self.kbd.append(kbd_entry)

            # Create an EXECUTE instruction to trigger the event
            self._kosmos.dt.pes.execute(action=self.kbd.action_event.SEND)

            # Add an instruction to wait until the end of previous KBD event
            self.kbd.pes_wait_kbd()
        # end if
        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def multiple_keys_press

    def multiple_keys_release(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_release``
        if delay is not None:
            super().multiple_keys_release(key_ids=key_ids, delay=delay)
        else:
            for key_id in key_ids:
                self._set_key_state(key_id, state=KeyState.BREAK, update_only=True)
                # Workaround : When there is no other action, filling one instruction in PES FIFO takes 1.14 us
                # while the execution of KBD_COMMAND_UPDATE by kbd module take 120 ns. Moreover in this loop there
                # are 2 PES instructions and 1 KBD instruction that are linked together. So the PES FIFO empties
                # faster than it can be filled, leading to errors.
                # That's why a 4us delay is added here to be sure the PES FIFO can be filled faster than the
                # instructions are consumed. This value was found empirically by analyzing the PES FIFO counter
                self._kosmos.dt.pes.delay(delay_s=DELAY_S_BETWEEN_KBD_COMMAND_UPDATE)
            # end for

            # Prepare Send command to KBD controller
            kbd_entry = kbd_entry_t()
            kbd_entry.bit.command = KBD_COMMAND_SEND

            # Add KBD instruction to buffer
            self.kbd.append(kbd_entry)

            # Create an EXECUTE instruction to trigger the event
            self._kosmos.dt.pes.execute(action=self.kbd.action_event.SEND)

            # Add an instruction to wait until the end of previous KBD event
            self.kbd.pes_wait_kbd()
        # end if
        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def multiple_keys_release

    def perform_action_list(self, action_list, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                            delay=ButtonStimuliInterface.DEFAULT_DURATION):
        # See ``ButtonStimuliInterface.perform_action_list``
        is_offline_enabled = self._kosmos.dt.sequencer.offline_mode
        if not is_offline_enabled:
            self._kosmos.dt.sequencer.offline_mode = True
        # end if

        super().perform_action_list(action_list=action_list, duration=duration, delay=delay)

        if not is_offline_enabled:
            self._kosmos.dt.sequencer.offline_mode = False
            self._kosmos.dt.sequencer.play_sequence()
        # end if
    # end def perform_action_list

    def perform_action_list_with_multiple_delays(self, action_list):
        # See ``ButtonStimuliInterface.perform_action_list_with_multiple_delays``
        is_offline_enabled = self._kosmos.dt.sequencer.offline_mode
        if not is_offline_enabled:
            self._kosmos.dt.sequencer.offline_mode = True
        # end if

        super().perform_action_list_with_multiple_delays(action_list)

        if not is_offline_enabled:
            self._kosmos.dt.sequencer.offline_mode = False
            self._kosmos.dt.sequencer.play_sequence()
        # end if
    # end def perform_action_list_with_multiple_delays

    def _set_key_state(self, key_id, state, immediate_execution=True, update_only=False):
        """
        Change the switch state of a given key, based on its row & col indexes.

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
        bank, lane, addr = self.get_bank_lane_addr(key_id)

        # Compute new lanes state
        lanes = self._compute_new_lanes_state(bank=bank, addr=addr, lane=lane, state=state)

        # Send lanes update
        if lanes != self.memory_cache[bank][addr]:
            # Debug print
            if self.verbose:
                self._set_key_state_debug_print(key_id=key_id, state=state)
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
                self._kosmos.dt.pes.execute(action=self.kbd.action_event.SEND)

                # Add an instruction to wait until the end of previous KBD event
                self.kbd.pes_wait_kbd()
            # end if
        # end if

        # Save Fn key lock state
        if self.fn_pressed and state == KeyState.MAKE and (
                key_id in [self._keyboard_layout.FN_KEYS[x] for x in
                           [KEY_ID.FN_LOCK, KEY_ID.FN_INVERSION_CHANGE] if x in self._keyboard_layout.FN_KEYS.keys()]):
            # C&P: Toggle Fn-Lock with the Fn-ESC command.
            self.fn_locked = not self.fn_locked
        # end if

        # Save Fn key pressed state
        if key_id == KEY_ID.FN_KEY:
            self.fn_pressed = (state == KeyState.MAKE)
        # end if
    # end def _set_key_state

    @abstractmethod
    def _set_key_state_debug_print(self, key_id, state):
        """
        Helper method to print the key state on the console. Refer to `_set_key_state` method.

        :param key_id: The target key be set to ON or OFF
        :type key_id: ``KEY_ID``
        :param state: BREAK (off, released) or MAKE (on, pressed)
        :type state: ``KeyState``
        """
        raise NotImplementedAbstractMethodError()
    # end def _set_key_state_debug_print

    def _compute_new_lanes_state(self, bank, addr, lane, state):
        """
        Compute new lanes state, based on the key state and on bank, addr and lane values.

        :param bank: Bank value
        :type bank: ``int``
        :param addr: Addr value
        :type addr: ``int``
        :param lane: Lane value
        :type lane: ``int``
        :param state: BREAK (off, released) or MAKE (on, pressed)
        :type state: ``KeyState``

        :return: new lanes state, based on the key state and on bank, addr and lane values
        :rtype: ``int``

        :raise ``AssertionError``: Out-of-bound lanes value
        """
        lanes = self.memory_cache[bank][addr]
        switch = 1 << lane

        if state == KeyState.MAKE and not (lanes & switch):
            # Turn switch ON
            lanes |= switch
        elif state == KeyState.BREAK and (lanes & switch):
            # Turn switch OFF
            lanes &= ~switch & self._lanes_mask
        # end if
        assert 0 <= lanes <= self._lanes_mask, f'Invalid lanes={lanes:#04x}, with lanes_mask={self._lanes_mask:#04x}.'

        return lanes
    # end def _compute_new_lanes_state

    @abstractmethod
    def get_bank_lane_addr(self, key_id):
        """
        Compute the bank, lane and address values for the given KEY_ID.

        Refer to the System Level Specification document referenced in the description of the class.

        :param key_id: The target key
        :type key_id: ``KEY_ID``

        :return: bank, lane and address values
        :rtype: ``tuple[int, int, int]``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_bank_lane_addr
# end class KosmosKeyMatrixEmulatorMixin


class KosmosKeyMatrixEmulator(KosmosKeyMatrixEmulatorMixin):
    """
    KeyMatrix emulator leveraging Kosmos test instrument (i.e. granddaughter board)

    Refer to the System Level Specification document
      KEYBOARD MATRIX CONTROLLER IP MODULE II
      https://docs.google.com/document/d/1yRsmBT0WLcmUFKmsOk50_oxwRLvlRtWfJDsCTSFPhZY
    """

    # Update type hint
    kbd: KbdMatrixModule
    keyboard_layout: Type[CommonKeyMatrix]

    def __init__(self, kosmos, fw_id, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: Invalid keyboard_layout
        """
        super().__init__(kosmos=kosmos, fw_id=fw_id, verbose=verbose, kbd=kosmos.dt.kbd_matrix)

        assert issubclass(self.keyboard_layout, CommonKeyMatrix), self.keyboard_layout
        assert self.keyboard_layout.KEYS, self.keyboard_layout.KEYS
    # end def __init__

    def setup_defaults(self):
        """
        Set defaults settings
        """
        super().setup_defaults()
        self.send_default_memory_cache_to_fpga()
    # end def setup_defaults

    def send_default_memory_cache_to_fpga(self):
        """
        Send the default memory cache to the FPGA.
        """
        # Prepare Reset command to KBD controller
        self.kbd.enable_set_default()

        for bank_id, bank_id_memory_cache in enumerate(self.default_memory_cache):
            for addr_id, lanes in enumerate(bank_id_memory_cache):
                # Prepare register Update command to KBD controller
                kbd_entry = kbd_entry_t()
                kbd_entry.bit.lane = lanes
                kbd_entry.bit.addr = addr_id
                kbd_entry.bit.bank = bank_id
                kbd_entry.bit.command = KBD_COMMAND_UPDATE

                # Add KBD instruction to buffer
                self.kbd.append(kbd_entry)

                # Create an EXECUTE instruction to trigger the event
                self._kosmos.dt.pes.execute(action=self.kbd.action_event.SEND)

                # Add an instruction to wait until the end of previous KBD event
                self.kbd.pes_wait_kbd()

                # Workaround : When there is no other action, filling one instruction in PES FIFO takes 1.14 us
                # while the execution of KBD_COMMAND_UPDATE by kbd module take 120 ns. Moreover in this loop there
                # are 2 PES instructions and 1 KBD instruction that are linked together. So the PES FIFO empties
                # faster than it can be filled, leading to errors.
                # That's why a 4us delay is added here to be sure the PES FIFO can be filled faster than the
                # instructions are consumed. This value was found empirically by analyzing the PES FIFO counter
                self._kosmos.dt.pes.delay(delay_s=DELAY_S_BETWEEN_KBD_COMMAND_UPDATE)
            # end for
        # end for

        # Prepare Reset command to KBD controller
        self.kbd.disable_set_default()

        # Apply the previous instructions
        self._kosmos.dt.sequencer.play_sequence()
    # end def send_default_memory_cache_to_fpga

    def _set_key_state_debug_print(self, key_id, state):
        # See ``KosmosKeyMatrixEmulatorMixin._set_key_state_debug_print``
        bank, lane, addr = self.get_bank_lane_addr(key_id)
        lanes = self._compute_new_lanes_state(bank=bank, addr=addr, lane=lane, state=state)
        row, col = self.get_row_col_indexes(key_id)
        stdout.write(f'  {state.name:5s} {KEY_ID(key_id).name}: row={row}, col={col}, '
                     f'bank={bank}, addr={addr}, lane={lane}, lanes={lanes:#04x}\n')
    # end def _set_key_state_debug_print

    def get_row_col_indexes(self, key_id):
        """
        Compute the row and column indexes for the given KEY_ID.

        :param key_id: The target key
        :type key_id: ``KEY_ID``

        :return: The computed row and column indexes
        :rtype: ``tuple[int, int]``

        :raise ``NotImplementedError``: Unsupported key value `key_id`
        """
        if key_id in self._keyboard_layout.KEYS:
            col, row = self._keyboard_layout.KEYS[key_id]
        elif key_id in self.get_fn_keys():
            col, row = self._keyboard_layout.KEYS[self._keyboard_layout.FN_KEYS[key_id]]
        else:
            raise NotImplementedError(f'Unsupported key {repr(key_id)}.')
        # end if
        return row, col
    # end def get_row_col_indexes

    def get_bank_lane_addr(self, key_id):
        # See ``KosmosKeyMatrixEmulatorMixin.get_bank_lane_addr``
        row, col = self.get_row_col_indexes(key_id)

        row_count = self.kbd.settings.kbd_row_count
        col_count = self.kbd.settings.kbd_col_count
        bank_count = self.kbd.settings.kbd_bank_count
        lane_count = self.kbd.settings.kbd_lane_count
        addr_count = self.kbd.settings.kbd_addr_count

        assert 0 <= row < row_count, f'{key_id!r}: Row = {row} is out of bounds [0, {row_count - 1}].'
        assert 0 <= col < col_count, f'{key_id!r}: Col = {col} is out of bounds [0, {col_count - 1}].'

        bank = 1 if row >= (row_count // 2) else 0
        lane = (row % (row_count // 2)) >> 1
        addr = (col << 1) | (row & 1)

        assert 0 <= bank < bank_count, f'{key_id!r}: Bank = {bank} is out of bounds [0, {bank_count - 1}].'
        assert 0 <= lane < lane_count, f'{key_id!r}: Lane = {lane} is out of bounds [0, {lane_count - 1}].'
        assert 0 <= addr < addr_count, f'{key_id!r}: Addr = {addr} is out of bounds [0, {addr_count - 1}].'

        return bank, lane, addr
    # end def get_bank_lane_addr
# end class KosmosKeyMatrixEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
