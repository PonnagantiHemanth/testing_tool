#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.dualkeymatrixemulator_test
:brief: Test for Kosmos Dual Keymatrix Emulator (GTECH KBD + MATRIX KBD)
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta

from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.kosmos.dualkeymatrixemulator import KosmosDualKeyMatrixEmulator
from pyraspi.services.kosmos.kosmos import FPGA_CURRENT_CLOCK_FREQ
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.kbdgtech_test import GALVATRON_KBD_FW_ID
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_SEND
from pyraspi.services.kosmos.protocol.generated.messages import KBD_COMMAND_UPDATE
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_delay_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_execute_t
from pyraspi.services.kosmos.protocol.generated.messages import pes_instruction_wait_t
from pyraspi.services.kosmos.test.gtechkeymatrixemulator_test import GtechKeymatrixEmulatorAbstractTestCase
from pyraspi.services.kosmos.test.gtechkeymatrixemulator_test import VERBOSE


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class DualKeymatrixEmulatorAbstractTestCase:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.test.gtechkeymatrixemulator_test.GtechKeymatrixEmulatorAbstractTestCase``
    """
    kbd_emu: KosmosDualKeyMatrixEmulator

    @require_kosmos_device(DeviceName.KBD_MATRIX)
    @require_kosmos_device(DeviceName.KBD_GTECH)
    class BaseTestCase(metaclass=ABCMeta):
        """
        Base TestCase class
        """
        @classmethod
        def _setup_emulator_under_test(cls):
            """
            Setup the Emulator under test
            """
            cls.kbd_emu = KosmosDualKeyMatrixEmulator(kosmos=cls.kosmos, fw_id=GALVATRON_KBD_FW_ID, verbose=VERBOSE)
        # end def _setup_emulator_under_test
    # end class BaseTestCase
# end class DualKeymatrixEmulatorAbstractTestCase


class DualKeymatrixEmulatorGtechLegacyModeTestCase(DualKeymatrixEmulatorAbstractTestCase.BaseTestCase,
                                                   GtechKeymatrixEmulatorAbstractTestCase.LegacyKbdGtechBaseTestCase):
    """
    Kosmos Dual Keymatrix Emulator test (KBD Gtech Module Test Class related to KBD functional mode: Legacy)
    (Key Press & Key Release ony).

    This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
    """
    pass  # Refer to test  implementation in ``GtechKeymatrixEmulatorAbstractTestCase.LegacyKbdGtechBaseTestCase``
# end class DualKeymatrixEmulatorGtechLegacyModeTestCase


class DualKeymatrixEmulatorGtechAnalogModeTestCase(DualKeymatrixEmulatorAbstractTestCase.BaseTestCase,
                                                   GtechKeymatrixEmulatorAbstractTestCase.AnalogKbdGtechBaseTestCase):
    """
    Kosmos Dual Keymatrix Emulator test (KBD Gtech Module Test Class related to KBD functional mode: Analog)
    (Key Release: displacement level 0 / Key Press displacement level 40)

    This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
    """
    pass  # Refer to test  implementation in ``GtechKeymatrixEmulatorAbstractTestCase.AnalogKbdGtechBaseTestCase``
# end class DualKeymatrixEmulatorGtechAnalogModeTestCase


class GalvanicKbdGtechModuleTestCase(DualKeymatrixEmulatorAbstractTestCase.BaseTestCase,
                                     GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase):
    """
    Kosmos KBD Gtech Module Test Class related to KBD functional mode: Galvanic key matrix (keyboard's top row)

    This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
    """
    @property
    def key_ids_under_test(self):
        # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.key_ids_under_test``
        return self.kbd_emu.galvanic_keys
    # end def property getter key_ids_under_test

    def test_get_bank_lane_addr(self):
        # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_get_bank_lane_addr``
        pass  # Validation test skipped for KBD_MATRIX module
    # end def test_get_bank_lane_addr

    def test_release_all(self):
        # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_release_all``
        key_id = KEY_ID.PLAY_PAUSE
        self.kbd_emu.key_press(key_id=key_id)

        self.kbd_emu.release_all()
    # end def test_release_all

    def test_release_all_complete(self):
        # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_release_all_complete``

        # Press all keys sequentially
        for key_id in self.key_ids_under_test.keys():
            self.kbd_emu.key_press(key_id=key_id)
        # end for

        # Release all keys at once
        self.kbd_emu.release_all()
    # end def test_release_all_complete

    def test_dimming_key(self):
        """
        Validate keystroke stimuli for ``KEY_ID.DIMMING_KEY``
        """
        self.kbd_emu.keystroke(key_id=KEY_ID.DIMMING_KEY)
    # end def test_dimming_key

    def test_play_pause(self):
        """
        Validate keystroke stimuli for ``KEY_ID.PLAY_PAUSE``
        """
        self.kbd_emu.keystroke(key_id=KEY_ID.PLAY_PAUSE)
    # end def test_play_pause

    def test_keyboard_mute(self):
        """
        Validate keystroke stimuli for ``KEY_ID.KEYBOARD_MUTE``
        """
        self.kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_MUTE)
    # end def test_keyboard_mute

    def test_game_mode_key(self):
        """
        Validate keystroke stimuli for ``KEY_ID.GAME_MODE_KEY``
        """
        self.kbd_emu.keystroke(key_id=KEY_ID.GAME_MODE_KEY)
    # end def test_game_mode_key

    def test_prev_track(self):
        """
        Validate keystroke stimuli for ``KEY_ID.PREV_TRACK``
        """
        self.kbd_emu.keystroke(key_id=KEY_ID.PREV_TRACK)
    # end def test_prev_track

    def test_next_track(self):
        """
        Validate keystroke stimuli for ``KEY_ID.NEXT_TRACK``
        """
        self.kbd_emu.keystroke(key_id=KEY_ID.NEXT_TRACK)
    # end def test_next_track
# end class GalvanicKbdGtechModuleTestCase


class DualKeymatrixEmulatorTestCase(DualKeymatrixEmulatorAbstractTestCase.BaseTestCase,
                                    GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase):
    """
    Kosmos Dual Keymatrix Module Test Class related to KBD functional modes:
     - Galvanic key matrix (keyboard's top row)
     - Gtech Analog key matrix (keyboard's bottom rows)

    This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
    """
    def setUp(self):
        """
        Setup test
        """
        super().setUp()

        # Change KBD Functional Mode from Legacy to Analog
        self.kbd_emu.kbd.func_mode_analog()
    # end def setUp

    def _test_multiple_keys(self, action):
        """
        Helper method to validate either:
         - ``KosmosDualKeyMatrixEmulator.multiple_keys_press`` method
         - ``KosmosDualKeyMatrixEmulator.multiple_keys_release`` method

        :param action: Action to do on a set of keys, either "PRESS" or "RELEASE"
        :type action: ``str``

        :raise ``AssertionError``: Invalid action
        """
        assert action in ("PRESS", "RELEASE"), action

        # Keys to be tested
        matrix_key_ids = [KEY_ID.KEYBOARD_MUTE, KEY_ID.NEXT_TRACK]
        gtech_key_ids = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B]
        key_ids = matrix_key_ids + gtech_key_ids

        # Prepare test sequence
        self.kbd_emu.kbd.dt.sequencer.offline_mode = True
        if action == "PRESS":
            self.kbd_emu.multiple_keys_press(key_ids=key_ids)
        else:
            self.kbd_emu.multiple_keys_release(key_ids=key_ids)
        # end if

        # Validate Matrix KBD Emulator instruction buffer
        self.assertEqual(len(matrix_key_ids) + 1, len(self.kbd_emu.emu_matrix.kbd._buffer),
                         msg=self.kbd_emu.emu_matrix.kbd._buffer)
        self.assertEqual(KBD_COMMAND_UPDATE, self.kbd_emu.emu_matrix.kbd._buffer[0].bit.command,
                         msg=self.kbd_emu.emu_matrix.kbd._buffer[0])
        self.assertEqual(KBD_COMMAND_UPDATE, self.kbd_emu.emu_matrix.kbd._buffer[1].bit.command,
                         msg=self.kbd_emu.emu_matrix.kbd._buffer[1])
        self.assertEqual(KBD_COMMAND_SEND, self.kbd_emu.emu_matrix.kbd._buffer[2].bit.command,
                         msg=self.kbd_emu.emu_matrix.kbd._buffer[2])

        # Validate Gtech KBD Emulator instruction buffer
        self.assertEqual(len(gtech_key_ids) + 1, len(self.kbd_emu.emu_gtech.kbd._buffer),
                         msg=self.kbd_emu.emu_gtech.kbd._buffer)
        self.assertEqual(KBD_COMMAND_UPDATE, self.kbd_emu.emu_gtech.kbd._buffer[0].bit.command,
                         msg=self.kbd_emu.emu_gtech.kbd._buffer[0])
        self.assertEqual(KBD_COMMAND_UPDATE, self.kbd_emu.emu_gtech.kbd._buffer[1].bit.command,
                         msg=self.kbd_emu.emu_gtech.kbd._buffer[1])
        self.assertEqual(KBD_COMMAND_SEND, self.kbd_emu.emu_gtech.kbd._buffer[2].bit.command,
                         msg=self.kbd_emu.emu_gtech.kbd._buffer[2])

        # Validate PES instruction buffer
        self.assertEqual(len(key_ids) * 3 + 2, len(self.kbd_emu.kbd.dt.pes._buffer),
                         msg=self.kbd_emu.kbd.dt.pes._buffer)

        # PES: validate Matrix KBD UPDATE instructions
        pes_buf_iter = iter(self.kbd_emu.kbd.dt.pes._buffer)
        for i in range(len(matrix_key_ids)):
            pes_exec = next(pes_buf_iter)
            self.assertIsInstance(pes_exec, pes_instruction_execute_t, msg=pes_exec)
            self.assertEqual(self.kbd_emu.emu_matrix.kbd.action_event.SEND.value, pes_exec.action_event, msg=pes_exec)

            pes_wait = next(pes_buf_iter)
            self.assertIsInstance(pes_wait, pes_instruction_wait_t, msg=pes_wait)
            self.assertEqual(self.kbd_emu.emu_matrix.kbd.resume_event.READY.value, pes_wait.resume_event, msg=pes_wait)

            pes_delay = next(pes_buf_iter)
            self.assertIsInstance(pes_delay, pes_instruction_delay_t, msg=pes_delay)
        # end for

        # PES: validate Gtech KBD UPDATE instructions
        for i in range(len(gtech_key_ids)):
            pes_exec = next(pes_buf_iter)
            self.assertIsInstance(pes_exec, pes_instruction_execute_t, msg=pes_exec)
            self.assertEqual(self.kbd_emu.emu_gtech.kbd.action_event.SEND.value, pes_exec.action_event, msg=pes_exec)

            pes_wait = next(pes_buf_iter)
            self.assertIsInstance(pes_wait, pes_instruction_wait_t, msg=pes_wait)
            self.assertEqual(self.kbd_emu.emu_gtech.kbd.resume_event.READY.value, pes_wait.resume_event, msg=pes_wait)

            pes_delay = next(pes_buf_iter)
            self.assertIsInstance(pes_delay, pes_instruction_delay_t, msg=pes_delay)
        # end for

        # PES: validate combined Gtech+Matrix KBD SEND instruction
        pes_exec = next(pes_buf_iter)
        self.assertIsInstance(pes_exec, pes_instruction_execute_t, msg=pes_exec)
        self.assertEqual(self.kbd_emu.emu_gtech.kbd.action_event.SEND.value +
                         self.kbd_emu.emu_matrix.kbd.action_event.SEND.value,
                         pes_exec.action_event, msg=pes_exec)

        # PES: validate combined Gtech+Matrix KBD WAIT READY instruction
        pes_wait = next(pes_buf_iter)
        self.assertIsInstance(pes_wait, pes_instruction_wait_t, msg=pes_wait)
        self.assertEqual(self.kbd_emu.emu_gtech.kbd.resume_event.READY.value +
                         self.kbd_emu.emu_matrix.kbd.resume_event.READY.value,
                         pes_wait.resume_event, msg=pes_wait)

        # Validate test sequence can be played
        self.kbd_emu.kbd.dt.sequencer.offline_mode = False
        self.kbd_emu.kbd.dt.sequencer.play_sequence()
    # end def _test_multiple_keys

    def test_multiple_keys_press(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_press`` method.
        """
        self._test_multiple_keys(action="PRESS")
    # end def test_multiple_keys_press

    def test_multiple_keys_release(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_release`` method.
        """
        self._test_multiple_keys(action="PRESS")  # keys must be pressed before we can test keys release
        self._test_multiple_keys(action="RELEASE")
    # end def test_multiple_keys_release

    def test_multiple_keys_fastest_delay(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_press`` and
        ``KosmosDualKeyMatrixEmulator.multiple_keys_release`` methods,
        setting the delay argument to the minimum duration allowed.

        No FIFO underrun shall occur durin the test.
        """
        key_ids = self.kbd_emu.connected_key_ids
        delay_s = 1 / FPGA_CURRENT_CLOCK_FREQ  # smallest delay
        self.kbd_emu.multiple_keys_press(key_ids=key_ids, delay=delay_s)
        self.kbd_emu.multiple_keys_release(key_ids=key_ids, delay=delay_s)
    # end def test_multiple_keys_fastest_delay
# end class DualKeymatrixEmulatorTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
