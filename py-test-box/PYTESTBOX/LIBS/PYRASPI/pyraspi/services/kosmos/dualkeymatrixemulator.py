#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.dualkeymatrixemulator
:brief: Kosmos Dual Keymatrix Emulator Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/04/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from typing import Iterable
from typing import Type

from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keybaordlayout import AnalogKeyMatrix
from pylibrary.emulator.keybaordlayout import COL_ROW_UNDEFINED
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.daemon import Daemon
from pyraspi.services.keyboardemulator import KeyState
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.gtechkeymatrixemulator import KosmosGtechKeyMatrixEmulator
from pyraspi.services.kosmos.keymatrixemulator import DELAY_S_BETWEEN_KBD_COMMAND_UPDATE
from pyraspi.services.kosmos.keymatrixemulator import DELAY_S_POST_RELEASE_ALL
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
from pyraspi.services.kosmos.module.kbdmatrix import KbdMatrixModule
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_RESET
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_SEND
from pyraspi.services.kosmos.protocol.generated.messages import kbd_entry_t
from pyraspi.services.kosmos.utils import pretty_list


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosDualKeyMatrixEmulator(KeyboardMixin):
    """
    Dual Keymatrix Emulator leveraging the following two Kosmos emulators:
     - Keymatrix Emulator (via GDB board)
     - Gtech Keymatrix Emulator - Analog Switch (via PODS board / PIO module)
    """

    # Type hints: Instances of underlying Keyboard Emulators
    emu_matrix: KosmosKeyMatrixEmulator
    emu_gtech: KosmosGtechKeyMatrixEmulator

    keyboard_layout: Type[AnalogKeyMatrix]

    def __init__(self, kosmos, fw_id, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: multiple source of error:
         - If not running on a Kosmos hardware
         - Invalid keyboard instance type
         - Invalid keyboard layout composition
        """
        assert Daemon.is_host_kosmos(), 'This class supports only Kosmos hardware'

        # Validate presence of the two hardware KBD emulators
        assert isinstance(kosmos.dt.kbd_matrix, KbdMatrixModule), kosmos.dt.kbd_matrix
        assert isinstance(kosmos.dt.kbd_gtech, KbdGtechModule), kosmos.dt.kbd_gtech

        # Instantiate the two emulators
        self.emu_matrix = KosmosKeyMatrixEmulator(kosmos=kosmos, fw_id=fw_id, verbose=verbose)
        self.emu_gtech = KosmosGtechKeyMatrixEmulator(kosmos=kosmos, fw_id=fw_id, verbose=verbose)

        # Key layout validation: 1) Analog keys must be marked as undefined in matrix keys list
        for key_id in self.keyboard_layout.KEYID_2_CHAINID:
            assert self.keyboard_layout.KEYS[key_id] is COL_ROW_UNDEFINED, key_id
        # end for

        # Key layout validation: 2) Undefined matrix keys must be defined in analog keys list.
        # 3) Defined matrix keys must be absent from analog keys list.
        for key_id, col_row_mapping in self.keyboard_layout.KEYS.items():
            if col_row_mapping is COL_ROW_UNDEFINED:
                assert key_id in self.keyboard_layout.KEYID_2_CHAINID, key_id
            else:
                assert key_id not in self.keyboard_layout.KEYID_2_CHAINID, key_id
            # end if
        # end for

        # Prepare mapping of valid galvanic key_ids
        self.galvanic_keys = {key_id: col_row_mapping
                              for key_id, col_row_mapping in self.keyboard_layout.KEYS.items()
                              if col_row_mapping is not COL_ROW_UNDEFINED}

        # Init mixin class
        super().__init__(fw_id=fw_id, verbose=verbose)
        self.setup_connected_key_ids()
    # end def __init__

    def __getattr__(self, name):
        """
        Redirection of KeyboardMixin class attributes and methods to the KosmosGtechKeyMatrixEmulator instance.
        All calls to methods and attributes that are not already defined in this class instance will be redirected to
        the KosmosGtechKeyMatrixEmulator underlying instance `self.emu_gtech`.

        Note: ``AttributeError`` is raised if attribute 'name' was not found within `self.emu_gtech`

        :param name: Attribute name
        :type name: ``str``

        :return: The value of the given attribute
        :rtype: ``Any``
        """
        return getattr(self.emu_gtech, name)
    # end def __getattr__

    @property
    def verbose(self):
        """
        Get verbose mode of either emulators.

        :return: Verbose mode
        :rtype: ``bool``
        """
        return self.emu_matrix.verbose or self.emu_gtech.verbose
    # end def property getter verbose

    @verbose.setter
    def verbose(self, value):
        """
        Set verbose mode of both emulators.

        :param value: Verbose mode, set True to enable
        :type value: ``bool``
        """
        self.emu_matrix.verbose = value
        self.emu_gtech.verbose = value
    # end def property setter verbose

    def key_id_2_emu(self, key_id):
        """
        Return the Keymatrix emulator instance to use for the given Key ID.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID or int``

        :return: a Keymatrix emulator instance
        :rtype: ``KosmosKeyMatrixEmulator or KosmosGtechKeyMatrixEmulator``

        :raise ``AssertionError``: If the given Key ID does not belong to either Gtech or Keymatrix Emulators
        """
        assert key_id in self.keyboard_layout.KEYS, f"Key {key_id!r} is not set in either Analog or Matrix layouts"
        return self.emu_matrix if key_id in self.galvanic_keys else self.emu_gtech
    # end def key_id_2_emu

    def key_ids_2_emu(self, key_ids):
        """
        Return the Keymatrix emulator instance to use for the given collection of Key ID.

        Limitation: all key_ids must belong to the same KBD Emulator key layout,
                    for the sake of implementation simplicity.

        :param key_ids: Collection of key identifiers
        :type key_ids: ``Iterable[KEY_ID or int]``

        :return: a Keymatrix emulator instance
        :rtype: ``KosmosKeyMatrixEmulator or KosmosGtechKeyMatrixEmulator``

        :raise ``AssertionError``: If all the given keys are not set in either Analog or Matrix layouts.
        """
        if all(key_id in self.keyboard_layout.KEYID_2_CHAINID for key_id in key_ids):
            return self.emu_gtech
        elif all(key_id in self.galvanic_keys for key_id in key_ids):
            return self.emu_matrix
        else:
            raise AssertionError(f"All the given keys are not set in either Analog or Matrix layouts: "
                                 + pretty_list(key_ids, formatter=repr))
        # end if
    # end def key_ids_2_emu

    def setup_defaults(self):
        # See ``KosmosKeyMatrixEmulatorMixin.release_all``
        self.emu_matrix.setup_defaults()
        self.emu_gtech.setup_defaults()
    # end def setup_defaults

    def release_all(self, post_delay=DELAY_S_POST_RELEASE_ALL):
        # See ``ButtonStimuliInterface.release_all``

        # Update local memory cache (clear)
        self.emu_matrix._init_memory_cache()
        self.emu_gtech._init_memory_cache()

        # Prepare Reset command to KBD controller
        kbd_entry = kbd_entry_t()
        kbd_entry.bit.command = KBD_COMMAND_RESET

        # Add KBD instruction to buffer
        self.emu_matrix.kbd.append(kbd_entry)
        self.emu_gtech.kbd.append(kbd_entry)

        # Create an EXECUTE instruction to trigger the event
        self._kosmos.dt.pes.execute(action=(self.emu_matrix.kbd.action_event.SEND,
                                            self.emu_gtech.kbd.action_event.SEND))

        # Add an instruction to wait until the end of previous KBD event
        self._kosmos.dt.pes.wait(action=(self.emu_matrix.kbd.resume_event.READY,
                                         self.emu_gtech.kbd.resume_event.READY))

        # Eventually, wait until the product/platform can detect the release
        self._sleep(post_delay)

        # Apply the previous instructions
        self._kosmos.dt.sequencer.play_sequence(timeout=1 + post_delay)
    # end def release_all

    def keystroke(self, key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION, repeat=1,
                  delay=ButtonStimuliInterface.DEFAULT_DELAY):
        # See ``ButtonStimuliInterface.keystroke``
        emu = self.key_id_2_emu(key_id=key_id)
        emu.keystroke(key_id=key_id, duration=duration, repeat=repeat, delay=delay)
    # end def keystroke

    def key_press(self, key_id):
        # See ``ButtonStimuliInterface.key_press``
        emu = self.key_id_2_emu(key_id=key_id)
        emu.key_press(key_id=key_id)
    # end def key_press

    def key_release(self, key_id):
        # See ``ButtonStimuliInterface.key_release``
        emu = self.key_id_2_emu(key_id=key_id)
        emu.key_release(key_id=key_id)
    # end def key_release

    def multiple_keys_state(self, key_ids, state, delay=None):
        """
        Emulate pressing or releasing multiple keys.

        See ``ButtonStimuliInterface.multiple_keys_press``
        See ``ButtonStimuliInterface.multiple_keys_release``

        :param key_ids: List of unique identifier of the keys to emulate
        :type key_ids: ``list[KEY_ID or int]``
        :param state: expected state of the keys
        :type state: ``KeyState``
        :param delay: Delay between 2 consecutive key presses, in seconds - OPTIONAL
        :type delay: ``float or None``
        """
        if delay is not None:
            # Set offline_mode during the preparation of the test sequence, to generate only one test sequence.
            offline_mode_tmp = self._kosmos.dt.sequencer.offline_mode
            self._kosmos.dt.sequencer.offline_mode = True

            for key_id in key_ids:
                self._set_key_state(key_id=key_id, state=state)
                self._sleep(delay)
            # end for

            # Restore original offline_mode
            self._kosmos.dt.sequencer.offline_mode = offline_mode_tmp
        else:
            # Set containing the emulator instances required for this key_ids list
            emulators = set()

            for key_id in key_ids:
                emu = self.key_id_2_emu(key_id=key_id)
                emulators.add(emu)
                emu._set_key_state(key_id=key_id, state=state, update_only=True)
                # Workaround : When there is no other action, filling one instruction in PES FIFO takes 1.14 us
                # while the execution of KBD_COMMAND_UPDATE by kbd module take 120 ns. Moreover, in this loop there
                # are 2 PES instructions and 1 KBD instruction that are linked together. So the PES FIFO empties
                # faster than it can be filled, leading to errors.
                # That's why a 4us delay is added here to be sure the PES FIFO can be filled faster than the
                # instructions are consumed. This value was found empirically by analyzing the PES FIFO counter
                self._kosmos.dt.pes.delay(delay_s=DELAY_S_BETWEEN_KBD_COMMAND_UPDATE)
            # end for

            for emu in emulators:
                # Prepare Send command to KBD controller
                kbd_entry = kbd_entry_t()
                kbd_entry.bit.command = KBD_COMMAND_SEND

                # Add KBD instruction to buffer
                emu.kbd.append(kbd_entry)
            # end for

            # Create a combined EXECUTE instruction to trigger the event
            self._kosmos.dt.pes.execute(action=(emu.kbd.action_event.SEND for emu in emulators))

            # Add a combined instruction to wait until the end of previous KBD event
            self._kosmos.dt.pes.wait(action=(emu.kbd.resume_event.READY for emu in emulators))
        # end if

        # Start to play the defined scenario
        self._kosmos.dt.sequencer.play_sequence()
    # end def multiple_keys_state

    def multiple_keys_press(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_press``
        self.multiple_keys_state(key_ids=key_ids, state=KeyState.MAKE, delay=delay)
    # end def multiple_keys_press

    def multiple_keys_release(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_release``
        self.multiple_keys_state(key_ids=key_ids, state=KeyState.BREAK, delay=delay)
    # end def multiple_keys_release

    def _sleep(self, delay):
        # See ``KeyboardMixin._sleep``
        if delay is not None and delay > 0:
            self._kosmos.dt.pes.delay(delay_s=delay)
        # end if
    # end def _sleep

    def _set_key_state(self, key_id, state, immediate_execution=True, update_only=False):
        # See ``ButtonStimuliInterface._set_key_state``
        emu = self.key_id_2_emu(key_id=key_id)
        emu._set_key_state(key_id=key_id, state=state, immediate_execution=immediate_execution, update_only=update_only)
    # end def _set_key_state
# end class KosmosDualKeyMatrixEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
