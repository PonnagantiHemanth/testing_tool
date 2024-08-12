#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.kosmos.kbdgtech
:brief: Kosmos Gtech Keymatrix Emulator Integration Tests
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/03/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from itertools import islice
from itertools import pairwise
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HID_REPORTS
from pyhid.hid import HidConsumer
from pyhid.hid import HidKeyboard
from pyhid.hid import HidKeyboardBitmap
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.dualkeymatrixemulator import KosmosDualKeyMatrixEmulator
from pyraspi.services.kosmos.gtechkeymatrixemulator import GTECH_KEY_PRESS_LEVEL
from pyraspi.services.kosmos.gtechkeymatrixemulator import GTECH_KEY_RELEASE_LEVEL
from pyraspi.services.kosmos.module.test.kbdgtech_test import GALVATRON_NO_HID_REPORTING_KEYS
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.tools.kosmos.kosmos import KosmosTestCase

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

VERBOSE = False  # Toggle verbose mode for this Integration Test file


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KosmosKbdGtechAbstractTestCase:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).
    """
    class KosmosKbdGtechTestCase(KosmosTestCase, metaclass=ABCMeta):
        """
        Kosmos Gtech Keymatrix Emulator Integration Tests.

        Kosmos Gtech Keymatrix Emulator Specifications:
            https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc/view

        NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY END-PRODUCT SPECIFICATIONS.
        """

        # Update type hint
        button_stimuli_emulator: KosmosDualKeyMatrixEmulator

        max_key_count_per_hid_report = 26  # maximum number of pressed key that can be reported on a HID Keyboard report

        @classmethod
        def setUpClass(cls):
            """
            Setup test class
            """
            super().setUpClass()
            assert isinstance(cls.button_stimuli_emulator, KosmosDualKeyMatrixEmulator), cls.button_stimuli_emulator

            cls.button_stimuli_emulator.verbose = VERBOSE

            # Setup feature 0x4523 index
            cls.feature_4523_index, cls.feature_4523, _, _ = (DisableControlsByCIDXTestUtils.
                                                              HIDppHelper.get_parameters(test_case=cls))
        # end def setUpClass

        def setUp(self):
            """
            Handle test prerequisites
            """
            super().setUp()

            self.disable_game_mode()
        # end def setUp

        def disable_game_mode(self):
            """
            Disable game mode, via feature 0x4523

            Reference: ``pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx.
                         DisableControlsByCIDXTestCase.enable_game_mode``

            :raise ``AssertionError``: Game Mode state update failed
            """
            # query the current game mode
            get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
            if get_game_mode_rsp.game_mode_full_state.enabled:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Game Mode is currently enabled. Pressing the {KEY_ID.GAME_MODE_KEY!r} '
                                         f'key to disable it.')
                # ------------------------------------------------------------------------------------------------------

                # Press Game Mode key
                self.button_stimuli_emulator.keystroke(key_id=KEY_ID.GAME_MODE_KEY)

                # Validate Game Mode got disabled
                get_game_mode_rsp = DisableControlsByCIDXTestUtils.HIDppHelper.get_game_mode(test_case=self)
                assert not get_game_mode_rsp.game_mode_full_state.enabled, get_game_mode_rsp
            # end if
        # end def disable_game_mode

        @property
        @abstractmethod
        def key_ids_under_test(self):
            """
            Return a mapping of KEY_ID to be tested.

            :return: collection of KEY_ID to be tested
            :rtype: ``Dict[KEY_ID, int] or Dict[KEY_ID, Tuple[int, int]]``
            """
            raise NotImplementedAbstractMethodError()
        # end def property getter key_ids_under_test

        @features('Keyboard')
        @level('Tools')
        @services('DualKeyMatrix')
        def test_release_all(self):
            """
            Verify the release_all() method resets the keymatrix state after one key was pressed
            """
            key_id = next(key_id for key_id in self.key_ids_under_test
                          if key_id not in GALVATRON_NO_HID_REPORTING_KEYS)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, f'Key Press: {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_press(key_id=key_id)
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Execute release_all()')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.release_all()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the release of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end def test_release_all

        @features('Keyboard')
        @level('Tools')
        @services('DualKeyMatrix')
        def test_release_all_complete(self):
            """
            Verify the release_all() method resets the keymatrix state after the allowed maximum number of key keys
            was pressed concurrently.
            """
            test_keys = list(islice((key_id for key_id in self.key_ids_under_test
                                    if key_id not in GALVATRON_NO_HID_REPORTING_KEYS),
                                    self.max_key_count_per_hid_report))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, f'Prepare Test Sequence')
            # ----------------------------------------------------------------------------------------------------------
            # Prepare PES sequence
            self.kosmos.sequencer.offline_mode = True

            # Press each key
            for key_id in test_keys:
                self.kosmos.dt.pes.wait_go_signal()
                self.button_stimuli_emulator.key_press(key_id=key_id)
            # end for

            # Finally, release all keys
            self.kosmos.dt.pes.wait_go_signal()
            self.button_stimuli_emulator.release_all()

            # Finish preparing PES sequence
            self.kosmos.sequencer.offline_mode = False

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Run Test Sequence')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the press of all keys')
            # ----------------------------------------------------------------------------------------------------------
            for key_id in test_keys:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard report for the press of key {key_id!r}')
                # ------------------------------------------------------------------------------------------------------
                self.kosmos.dt.fpga.pulse_global_go_line()  # instruct FPGA to execute next KBD instruction
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))
            # end for

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Execute release_all()')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.dt.fpga.pulse_global_go_line()  # instruct FPGA to execute next KBD instruction
            self.kosmos.sequencer.wait_end_of_sequence()

            # HID Consumer key press report is sent when key is released, hence two back-to-back reports are received
            for retry in range(2):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID report for the simultaneous release of all keys'
                                          + (f' (retry: {retry})' if retry else ''))
                # ------------------------------------------------------------------------------------------------------
                hid_report = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                                   class_type=(HidKeyboard, HidKeyboardBitmap, HidConsumer))

                empty_hid_report = (HidKeyboard() if hid_report.name == 'HidKeyboard'
                                    else HidKeyboardBitmap() if hid_report.name == 'HidKeyboardBitmap'
                                    else HidConsumer())
                if empty_hid_report == hid_report:
                    break
                # end if
            # end for
            self.assertEqual(empty_hid_report, hid_report)
        # end def test_release_all_complete

        @features('Keyboard')
        @level('Tools')
        @services('DualKeyMatrix')
        def test_key_press_key_release_all_keys(self):
            """
            Press then release each available keys, while checking all HID reports.
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, f'Prepare Test Sequence: Verify key press then release for each keys')
            # ----------------------------------------------------------------------------------------------------------
            # Prepare PES sequence
            self.kosmos.sequencer.offline_mode = True

            # Press then Release each key
            self.kosmos.dt.pes.wait_go_signal()
            for key_id in self.key_ids_under_test:
                self.button_stimuli_emulator.key_press(key_id=key_id)
                self.kosmos.dt.pes.wait_go_signal()

                self.button_stimuli_emulator.key_release(key_id=key_id)
                self.kosmos.dt.pes.wait_go_signal()
            # end for

            # Execute PES sequence
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(block=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Run Test Sequence')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.dt.fpga.pulse_global_go_line()  # start test

            for key_id, key_pos in self.key_ids_under_test.items():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard report for the press of key {key_id!r} '
                                          f'(chain_id/col_row={key_pos})')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

                self.kosmos.dt.fpga.pulse_global_go_line()  # instruct FPGA to execute next KBD instruction

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check HID Keyboard report for the release of key {key_id!r} '
                                          f'(chain_id/col_row={key_pos})')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))

                self.kosmos.dt.fpga.pulse_global_go_line()  # instruct FPGA to execute next KBD instruction
            # end for
        # end def test_key_press_key_release_all_keys

        def _key_press_key_release_check_hid_reports(self, key_id):
            """
            Test routine, emulating a keystroke while checks the HID reports.

            :param key_id: The key identifier
            :type key_id: ``KEY_ID``
            """
            self.button_stimuli_emulator.key_press(key_id=key_id)
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            self.button_stimuli_emulator.key_release(key_id=key_id)
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end def _key_press_key_release_check_hid_reports
    # end class KosmosKbdGtechTestCase
# end class KosmosKbdGtechAbstractTestCase


class KosmosKbdGtechLegacyTestCase(KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase):
    """
    Kosmos Gtech Keymatrix Emulator Integration Tests. (Legacy Mode)

    Kosmos Gtech Keymatrix Emulator Specifications:
        https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc/view

    NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY END-PRODUCT SPECIFICATIONS.
    """
    @property
    def key_ids_under_test(self):
        # See ``KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase.key_ids_under_test``
        return self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID
    # end def property getter key_ids_under_test
# end class KosmosKbdGtechLegacyTestCase


class KosmosKbdGtechAnalogTestCase(KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase):
    """
    Kosmos Gtech Keymatrix Emulator Integration Tests. (Analog Mode)

    Kosmos Gtech Keymatrix Emulator Specifications:
        https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc/view

    NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY END-PRODUCT SPECIFICATIONS.
    """

    # Update type hint
    button_stimuli_emulator: KosmosDualKeyMatrixEmulator

    def setUp(self):
        """
        Setup test
        """
        super().setUp()

        # Change KBD Functional Mode from Legacy to Analog
        self.button_stimuli_emulator.kbd.func_mode_analog()
    # end def setUp

    @property
    def key_ids_under_test(self):
        # See ``KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase.key_ids_under_test``
        return self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID
    # end def property getter key_ids_under_test

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    def test_key_displacement(self):
        """
        Validate `KbdGtechModule.key_displacement` method, while sequencer mode is ONLINE.
        Validate KBD instructions: KBD_COMMAND_UPDATE_SEND.

        Loop though all keys. Set one key at a time to a displacement level 40, then to 0.
        """
        for key_id in self.key_ids_under_test:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set key {key_id!r} displacement {GTECH_KEY_PRESS_LEVEL!r} (pressed)')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=key_id, displacement=GTECH_KEY_PRESS_LEVEL)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the press of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set key {key_id!r} displacement {GTECH_KEY_RELEASE_LEVEL!r} (released)')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.key_displacement(key_id=key_id, displacement=GTECH_KEY_RELEASE_LEVEL)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the release of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for
    # end def test_key_displacement

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    def test_key_displacement_all_keys(self):
        """
        Validate `KbdGtechModule.key_displacement` method, while sequencer mode is OFFLINE.
        Validate KBD instructions: KBD_COMMAND_UPDATE_SEND.

        Loop though all keys. Set one key at a time to a displacement level 40, then to 0.
        """
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Prepare Test Sequence')
        # ----------------------------------------------------------------------------------------------------------

        # Prepare PES sequence
        self.kosmos.sequencer.offline_mode = True

        # Press then Release all keys
        for key_id in self.key_ids_under_test:
            for displacement in (GTECH_KEY_PRESS_LEVEL, GTECH_KEY_RELEASE_LEVEL):
                self.kosmos.dt.pes.wait_go_signal()
                self.button_stimuli_emulator.key_displacement(key_id=key_id, displacement=displacement)
            # end for
        # end for

        # Finish preparing PES sequence
        self.kosmos.sequencer.offline_mode = False

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Run Test Sequence')
        # ----------------------------------------------------------------------------------------------------------
        self.kosmos.sequencer.play_sequence(block=False)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard report for the press then release of each keys')
        # ----------------------------------------------------------------------------------------------------------
        for key_id in self.key_ids_under_test:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the press of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.dt.fpga.pulse_global_go_line()  # instruct FPGA to execute next KBD instruction
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report for the release of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.dt.fpga.pulse_global_go_line()  # instruct FPGA to execute next KBD instruction
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for
        self.kosmos.sequencer.wait_end_of_sequence()
    # end def test_key_displacement_all_keys
# end class KosmosKbdGtechAnalogTestCase


class KosmosKbdGtechGalvanicTestCase(KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase):
    """
    Kosmos Gtech Keymatrix Emulator Integration Tests. (Galvanic key matrix)

    Kosmos Gtech Keymatrix Emulator Specifications:
        https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc/view

    NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY END-PRODUCT SPECIFICATIONS.
    """

    max_key_count_per_hid_report = 2  # maximum number of pressed key that can be reported on a HID Consumer report

    @property
    def key_ids_under_test(self):
        # See ``KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase.key_ids_under_test``
        return self.button_stimuli_emulator.galvanic_keys
    # end def property getter key_ids_under_test

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.DIMMING_KEY,))
    def test_dimming_key(self):
        """
        Validate keystroke stimuli for ``KEY_ID.DIMMING_KEY``
        """
        self._key_press_key_release_check_hid_reports(key_id=KEY_ID.DIMMING_KEY)
    # end def test_dimming_key

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.PLAY_PAUSE,))
    def test_play_pause(self):
        """
        Validate keystroke stimuli for ``KEY_ID.PLAY_PAUSE``
        """
        self._key_press_key_release_check_hid_reports(key_id=KEY_ID.PLAY_PAUSE)
    # end def test_play_pause

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.KEYBOARD_MUTE,))
    def test_keyboard_mute(self):
        """
        Validate keystroke stimuli for ``KEY_ID.KEYBOARD_MUTE``
        """
        self._key_press_key_release_check_hid_reports(key_id=KEY_ID.KEYBOARD_MUTE)
    # end def test_keyboard_mute

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.GAME_MODE_KEY,))
    def test_game_mode_key(self):
        """
        Validate keystroke stimuli for ``KEY_ID.GAME_MODE_KEY``
        """
        self._key_press_key_release_check_hid_reports(key_id=KEY_ID.GAME_MODE_KEY)
    # end def test_game_mode_key

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.PREV_TRACK,))
    def test_prev_track(self):
        """
        Validate keystroke stimuli for ``KEY_ID.PREV_TRACK``
        """
        self._key_press_key_release_check_hid_reports(key_id=KEY_ID.PREV_TRACK)
    # end def test_prev_track

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.NEXT_TRACK,))
    def test_next_track(self):
        """
        Validate keystroke stimuli for ``KEY_ID.NEXT_TRACK``
        """
        self._key_press_key_release_check_hid_reports(key_id=KEY_ID.NEXT_TRACK)
    # end def test_next_track
# end class KosmosKbdGtechGalvanicTestCase


class KosmosDualKbdTestCase(KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase):
    """
    Kosmos Dual Keymatrix Emulator Integration Tests. (Gtech + Galvanic key matrix)

    Kosmos Gtech Keymatrix Emulator Specifications:
        https://docs.google.com/document/d/1rLcB5X7VNgh3wG0p3ZGXUQwhK9sys4-xTgk_O_TdZFc/view

    NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY END-PRODUCT SPECIFICATIONS.
    """

    @property
    def key_ids_under_test(self):
        # See ``KosmosKbdGtechAbstractTestCase.KosmosKbdGtechTestCase.key_ids_under_test``
        return (self.button_stimuli_emulator.keyboard_layout.KEYID_2_CHAINID |
                self.button_stimuli_emulator.galvanic_keys)
    # end def property getter key_ids_under_test


    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_B))
    def test_multiple_keys_press_then_release(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_press`` then
         ``KosmosDualKeyMatrixEmulator.multiple_keys_release`` methods, without setting the `delay` argument.
        """
        # Keys to be tested
        key_ids = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_B]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Call multiple_keys_press() on keys: ' + ', '.join(map(repr,key_ids)))
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=key_ids)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard report for the press of key {KEY_ID.KEYBOARD_A!r} + '
                                  f'{KEY_ID.KEYBOARD_B!r}')
        # ----------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_A, MAKE),
                                                      raise_exception=False)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_B, MAKE))

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Consumer report for the press of key {KEY_ID.KEYBOARD_MUTE!r}')
        # ----------------------------------------------------------------------------------------------------------
        sleep(0.5)  # HID Consumer report are sent after 500 ms delay if no other key combination is made
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_MUTE, MAKE))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Call multiple_keys_release() on keys: ' + ', '.join(map(repr,key_ids)))
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=key_ids)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Keyboard report for the release of key {KEY_ID.KEYBOARD_A!r} + '
                                  f'{KEY_ID.KEYBOARD_B!r}')
        # ----------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_A, BREAK),
                                                      raise_exception=False)
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_B, BREAK))

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check HID Consumer report for the release of key {KEY_ID.KEYBOARD_MUTE!r}')
        # ----------------------------------------------------------------------------------------------------------
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                      key=KeyMatrixTestUtils.Key(KEY_ID.KEYBOARD_MUTE, BREAK))
    # end def test_multiple_keys_press_then_release

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_B))
    def test_multiple_keys_press_delayed(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_press`` method, making use of the `delay` argument.
        This test only validates the HID reports content, not the key press timings.
        """
        # Keys to be tested
        key_ids = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_B]

        # Delay between key presses
        delay_s = 0.6

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Call multiple_keys_press() on keys: ' + ', '.join(map(repr,key_ids)))
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_press(key_ids=key_ids, delay=delay_s)

        for key_id in key_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard/Consumer report content for the press of key '
                                      f'{key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE))
        # end for
    # end def test_multiple_keys_press_delayed

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_B))
    def test_multiple_keys_release_delayed(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_release`` method, making use of the `delay` argument.
        This test only validates the HID reports content, not the key press timings.
        """
        # Keys to be tested
        key_ids = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_MUTE, KEY_ID.KEYBOARD_B]

        # Delay between key presses
        delay_s = 0.6

        # keys must be pressed before we can test keys release
        self.test_multiple_keys_press_delayed()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Call multiple_keys_release() on keys: ' + ', '.join(map(repr,key_ids)))
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(key_ids=key_ids, delay=delay_s)

        for key_id in key_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard/Consumer report for the release of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK))
        # end for
    # end def test_multiple_keys_release_delayed

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C))
    def test_multiple_keys_press_delayed_timing(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_press`` method, making use of the `delay` argument.
        This test only validates the key press timings, not the HID reports content.
        """
        # Keys to be tested
        key_ids = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C]

        # Delay between key presses
        delay_s = 0.6

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Call multiple_keys_press() on keys: ' + ', '.join(map(repr,key_ids)))
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.dt.sequencer.offline_mode = True
        self.kosmos.dt.pes.wait_go_signal()
        self.button_stimuli_emulator.multiple_keys_press(key_ids=key_ids, delay=delay_s)
        self.kosmos.dt.sequencer.offline_mode = False
        self.kosmos.dt.sequencer.play_sequence(block=False)

        hid_reports = []
        for key_id in key_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Waiting for HID Keyboard report for the press of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.dt.fpga.pulse_global_go_line()
            hid_msg = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                            class_type=HID_REPORTS)
            hid_reports.append(hid_msg)
        # end for

        # Validate delay after last key press
        self.assertFalse(self.kosmos.dt.sequencer.is_end_of_sequence())
        sleep(delay_s)
        self.assertTrue(self.kosmos.dt.sequencer.is_end_of_sequence())

        for i, (key1_id, key2_id) in enumerate(pairwise(key_ids)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report timing between the press of keys '
                                      f'{key1_id!r} and {key2_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            delta_s = (hid_reports[i + 1].timestamp - hid_reports[i].timestamp) / 10**9
            self.assertAlmostEqual(delta_s, delay_s, delta=0.1,
                                   msg=f'timing({key2_id!r}) - timing({key1_id!r}) should be equal to {delay_s} s')
        # end for
    # end def test_multiple_keys_press_delayed_timing

    @features('Keyboard')
    @level('Tools')
    @services('DualKeyMatrix')
    @services("RequiredKeys", (KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C))
    def test_multiple_keys_release_delayed_timing(self):
        """
        Validate ``KosmosDualKeyMatrixEmulator.multiple_keys_release`` method, making use of the `delay` argument.
        This test only validates the key press timings, not the HID reports content.
        """
        # Keys to be tested
        key_ids = [KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_B, KEY_ID.KEYBOARD_C]

        # Delay between key presses
        delay_s = 0.6

        # keys must be pressed before we can test keys release
        self.test_multiple_keys_press_delayed_timing()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Call multiple_keys_release() on keys: ' + ', '.join(map(repr, key_ids)))
        # --------------------------------------------------------------------------------------------------------------
        self.kosmos.dt.sequencer.offline_mode = True
        self.kosmos.dt.pes.wait_go_signal()
        self.button_stimuli_emulator.multiple_keys_release(key_ids=key_ids, delay=delay_s)
        self.kosmos.dt.sequencer.offline_mode = False
        self.kosmos.dt.sequencer.play_sequence(block=False)

        hid_reports = []
        for key_id in key_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Waiting for HID Keyboard report for the release of key {key_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.dt.fpga.pulse_global_go_line()
            hid_msg = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                            class_type=HID_REPORTS)
            hid_reports.append(hid_msg)
        # end for

        # Validate delay after last key release
        self.assertFalse(self.kosmos.dt.sequencer.is_end_of_sequence())
        sleep(delay_s)
        self.assertTrue(self.kosmos.dt.sequencer.is_end_of_sequence())

        for i, (key1_id, key2_id) in enumerate(pairwise(key_ids)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard report timing between the release of keys '
                                      f'{key1_id!r} and {key2_id!r}')
            # ----------------------------------------------------------------------------------------------------------
            delta_s = (hid_reports[i + 1].timestamp - hid_reports[i].timestamp) / 10 ** 9
            self.assertAlmostEqual(delta_s, delay_s, delta=0.1,
                                   msg=f'timing({key2_id!r}) - timing({key1_id!r}) should be equal to {delay_s} s')
        # end for
    # end def test_multiple_keys_release_delayed_timing
# end class KosmosDualKbdTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
