#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.hybridkeymatrixemulator_test
:brief: Tests for Kosmos Hybrid Key Matrix Controller
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2021/03/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyhid.hiddata import HidData
from pylibrary.emulator.characters import CHAR_TO_KEYID_MAP
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import KEYSTROKE
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import float_range
from pyraspi.services.kosmos.hybridkeymatrixemulator import KosmosHybridKeyMatrixEmulator
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.test.keymatrixemulator_test import KosmosKeyMatrixEmulatorTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
KBD_FW_ID = 'MPK20'  # Hospoa


@require_kosmos_device(DeviceName.KBD_MATRIX)
class KosmosHybridKeyMatrixEmulatorTestCase(KosmosKeyMatrixEmulatorTestCase):
    """
    Unitary Test for Kosmos Board Hybrid Key Matrix Controller.
    """
    _kbd_emu: KosmosHybridKeyMatrixEmulator
    _slider_emu: KosmosPowerSliderEmulator

    VERBOSE = True

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos board
        """
        super().setUpClass()

        # Key matrix should correctly be initialised here
        cls._kbd_emu = KosmosHybridKeyMatrixEmulator(kosmos=cls.kosmos, fw_id=KBD_FW_ID, verbose=cls.VERBOSE)

        cls._kbd_emu._init_optical_matrix()

        # Configure HID report
        HidData.configure(keyboard_report_type='HidKeyboard')

        # To uncomment if the Col7 is not properly driven by the hardware
        # cls._kbd_emu.key_press(KEY_ID.SIGNAL_N_OFF)
        cls._slider_emu = KosmosPowerSliderEmulator(kosmos=cls.kosmos, fw_id='MPK20')
        if cls._slider_emu is not None:
            cls._slider_emu.power_on()
        # end if

        sleep(0.05)
    # end def setUpClass

    @classmethod
    def tearDownClass(cls):
        """
        Close Kosmos board
        """
        super().tearDownClass()

        # To uncomment if the Col7 is not properly driven by the hardware
        # cls._kbd_emu.key_release(KEY_ID.SIGNAL_N_OFF)

        if cls._slider_emu is not None:
            cls._slider_emu.power_off()
            sleep(1)
        # end if
    # end def tearDownClass

    def test_power_on(self):
        """
        Simply power on the DUT and wait 2mn
        """
        sleep(120)
    # end def test_power_on

    def test_switch_to_ble(self):
        """
        Validate switching to BLE
        """
        self._kbd_emu.key_press(KEY_ID.BLE_CONNECTION_TOGGLE)
        sleep(5)
        self._kbd_emu.key_release(KEY_ID.BLE_CONNECTION_TOGGLE)
        sleep(60)
    # end def test_switch_to_ble

    def test_press_ble_ls2_loop(self):
        """
        Loop over the transition from BLE to LS2 5 time
        """
        for i in range(5):
            self._kbd_emu.key_press(KEY_ID.BLE_CONNECTION_TOGGLE)
            sleep(5)
            self._kbd_emu.key_release(KEY_ID.BLE_CONNECTION_TOGGLE)
            sleep(30)
            self._kbd_emu.key_press(KEY_ID.LS2_CONNECTION_TOGGLE)
            sleep(5)
            self._kbd_emu.key_release(KEY_ID.LS2_CONNECTION_TOGGLE)
            sleep(30)
        # end for
    # end def test_press_ble_ls2_loop

    def test_toggle_caps_lock(self):
        """
        Test toggling the Caps Lock key
        """
        self._kbd_emu.keystroke(KEY_ID.KEYBOARD_CAPS_LOCK)
    # end def test_toggle_caps_lock

    def test_press_o_u(self):
        """
        Test pressing and let "MAKE" the "O" and "U" keys for 5 seconds 5 times
        """
        for i in range(5):
            self._kbd_emu.key_press(KEY_ID.KEYBOARD_O)
            sleep(5)
            self._kbd_emu.key_release(KEY_ID.KEYBOARD_O)
            sleep(5)
            self._kbd_emu.key_press(KEY_ID.KEYBOARD_U)
            sleep(5)
            self._kbd_emu.key_release(KEY_ID.KEYBOARD_U)
            sleep(5)
            i = i+1
        # end for
    # end def test_press_o_u

    def test_user_action(self):
        """
        Validate user_action() method
        """
        self._kbd_emu.user_action()
    # end def test_user_action

    def test_keystroke(self):
        """
        Validate keystroke() method
        """
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_RETURN_ENTER, duration=.2, repeat=1, delay=None)
    # end def test_keystroke

    def test_key_press_release(self):
        """
        Validate key_press() and key_release() methods
        """
        for key_id in range(KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z + 1):
            self._kbd_emu.key_press(key_id=KEY_ID(key_id))
        # end for
        for key_id in range(KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z + 1):
            self._kbd_emu.key_release(key_id=KEY_ID(key_id))
        # end for
    # end def test_key_press_release

    def test_multiple_keys_press(self):
        """
        Validate multiple_keys_press() method
        """
        self._kbd_emu.multiple_keys_press(key_ids=[KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z])
    # end def test_multiple_keys_press

    def test_multiple_keys_release(self):
        """
        Validate multiple_keys_release() method
        """
        self._kbd_emu.multiple_keys_release(key_ids=[KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z])
    # end def test_multiple_keys_release

    def test_perform_action_list(self):
        """
        Validate perform_action_list() method
        """
        action_list = [(KEY_ID.KEYBOARD_A, MAKE), (KEY_ID.KEYBOARD_B, BREAK), (KEY_ID.KEYBOARD_C, KEYSTROKE)]
        self._kbd_emu.perform_action_list(action_list=action_list, delay=.2)
    # end def test_perform_action_list

    def test_perform_action_list_offline_mode(self):
        """
        Validate perform_action_list() method when offline mode is enabled
        """
        self.kosmos.sequencer.offline_mode = True
        action_list = [(KEY_ID.KEYBOARD_A, MAKE), (KEY_ID.KEYBOARD_B, BREAK), (KEY_ID.KEYBOARD_C, KEYSTROKE)]
        self._kbd_emu.perform_action_list(action_list=action_list, delay=.2)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self._check_hid_reports(action_list)
    # end def test_perform_action_list_offline_mode

    def test_alphabet_lowercase(self):
        """
        Validate all the letters of the alphabet in their lower case version.
        """
        for key_id in range(KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z + 1):
            self._kbd_emu.keystroke(key_id=KEY_ID(key_id), delay=.1)
        # end for
    # end def test_alphabet_lowercase

    def test_alphabet_uppercase(self):
        """
        Validate all the letters of the alphabet in their upper case version.
        """
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_CAPS_LOCK)
        for key_id in range(KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z + 1):
            self._kbd_emu.keystroke(key_id=KEY_ID(key_id), delay=.1)
        # end for
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_CAPS_LOCK)
    # end def test_alphabet_uppercase

    def test_numbers(self):
        """
        Validate keys emulating numbers from 1 to 9 plus 0.
        """
        for key_id in range(KEY_ID.KEYBOARD_1, KEY_ID.KEYBOARD_0 + 1):
            self._kbd_emu.keystroke(key_id=KEY_ID(key_id), delay=.1)
        # end for
    # end def test_numbers

    def test_keypad(self):
        """
        Validate keys linked to a keypad from 1 to 9 plus 0.
        """
        if not self._kbd_emu._keyboard_layout.HAS_KEYPAD:
            self.skipTest(f'{self._kbd_emu._keyboard_layout.__name__} keyboard layout has no keypad to be tested.')
        # end if

        for key_id in range(KEY_ID.KEYPAD_1_AND_END, KEY_ID.KEYPAD_0_AND_INSERT + 1):
            self._kbd_emu.keystroke(key_id=KEY_ID(key_id), delay=.1)
        # end for
    # end def test_keypad

    def test_special_key(self):
        """
        Validate 'fn' plus 'Volume up' 2 times
        """
        action_list = [(KEY_ID.FN_KEY, MAKE), (KEY_ID.KEYBOARD_VOLUME_UP, KEYSTROKE),
                       (KEY_ID.KEYBOARD_VOLUME_UP, KEYSTROKE), (KEY_ID.FN_KEY, BREAK)]
        self._kbd_emu.perform_action_list(action_list=action_list, delay=.2)
        self._check_hid_reports(action_list)
    # end def test_special_key

    def test_key_combination_ctrl_shift_u(self):
        """
        Validate key combination to force text in uppercase in notepad
        Ctrl + Shift + U
        """
        action_list = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE), (KEY_ID.KEYBOARD_LEFT_SHIFT, MAKE),
                       (KEY_ID.KEYBOARD_U, KEYSTROKE), (KEY_ID.KEYBOARD_LEFT_SHIFT, BREAK),
                       (KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]
        self._kbd_emu.perform_action_list(action_list=action_list, delay=.2)
        self._check_hid_reports(action_list)
    # end def test_key_combination_ctrl_shift_u

    def test_key_combination_ctrl_shift_left_arrow(self):
        """
        Validate key combination to select next word to the left in notepad
        Ctrl + Shift + Left Arrow
        """
        action_list = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE), (KEY_ID.KEYBOARD_LEFT_SHIFT, MAKE),
                       (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE), (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE),
                       (KEY_ID.KEYBOARD_LEFT_ARROW, KEYSTROKE), (KEY_ID.KEYBOARD_LEFT_SHIFT, BREAK),
                       (KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]
        self._kbd_emu.perform_action_list(action_list=action_list, delay=.2)
        self._check_hid_reports(action_list)
    # end def test_key_combination_ctrl_shift_left_arrow

    def test_notepad_shortcut_keys(self):
        """
        Validate some notepad shortcut keys
        - Ctrl + n: create a new tab
        - Write a 2-line text
        - Ctrl + a: select all
        - Tab: adds an indentation level to the active line or selection
        - Ctrl + Shift + U: converts the selection to upper case
        - Ctrl + '+': zoom
        """
        # Ctrl + n: create a new tab
        create_new_tab = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE), (KEY_ID.KEYBOARD_N, KEYSTROKE),
                          (KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]
        self._kbd_emu.perform_action_list(action_list=create_new_tab)
        # Write a 2-line text
        self._format_text('Equality and Environment\nWe strive to be responsible for our planet.\n')
        # Ctrl + a: select all
        select_all = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE), (KEY_ID.KEYBOARD_A, KEYSTROKE),
                      (KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]
        self._kbd_emu.perform_action_list(action_list=select_all)
        # Tab: adds an indentation level to the active line or selection
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_TAB)
        # Ctrl + Shift + U: converts the selection to upper case
        upper_case_convertion = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE), (KEY_ID.KEYBOARD_RIGHT_SHIFT, MAKE),
                                 (KEY_ID.KEYBOARD_U, KEYSTROKE), (KEY_ID.KEYBOARD_RIGHT_SHIFT, BREAK),
                                 (KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]
        self._kbd_emu.perform_action_list(action_list=upper_case_convertion)
        # Ctrl + '+': zoom in
        zoom_in_four_times = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE)] \
                             + CHAR_TO_KEYID_MAP['+'] * 4 \
                             + [(KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]

        self._kbd_emu.perform_action_list(action_list=zoom_in_four_times)
        # Ctrl + '-': zoom out
        zoom_out_four_times = [(KEY_ID.KEYBOARD_LEFT_CONTROL, MAKE)] \
                              + CHAR_TO_KEYID_MAP['-'] * 4 \
                              + [(KEY_ID.KEYBOARD_LEFT_CONTROL, BREAK)]
        self._kbd_emu.perform_action_list(action_list=zoom_out_four_times)
    # end def test_notepad_shortcut_keys

    def test_increase_typing_speed(self):
        """
        Validate the board is managing the delay between 2 keystrokes.
        """
        self.kosmos.sequencer.offline_mode = True
        for delay_str in float_range(first=0.2, last=0.04, step=-0.01):
            self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_A, duration=.05, repeat=2, delay=float(delay_str))
            self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_B, duration=.05, repeat=2, delay=float(delay_str))
        # end for
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        # end for
    # end def test_increase_typing_speed

    def test_typing_simple_text(self):
        """
        Check that a simple text could be converted into instructions
        """
        self.kosmos.sequencer.offline_mode = True
        text = 'We design experiences so you create, achieve and enjoy more.\n'
        self._format_text(text)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
    # end def test_typing_simple_text

    def _format_text(self, text):
        """
        Create the sequence of characters associated with the text in parameter.

        :param text: sentence to format
        :type text: ``str``

        :return: The list of keys to be pressed
        :rtype: ``list(KEY_ID)``
        """
        action_list = []
        for char in list(text):
            action_list.extend(CHAR_TO_KEYID_MAP[char])
        # end for
        self._kbd_emu.perform_action_list(action_list=action_list, duration=.05, delay=.05)
        return action_list
    # end def _format_text

    def test_typing_complex_text(self):
        """
        Check that a complex text could be converted into instructions
        """
        text = ['"You never really understand a person until you consider things from his point of view.\n',
                'Until you climb inside of his skin and walk around in it" \nTo Kill a Mockingbird by Harper Lee.\n']
        for sentence in text:
            self.kosmos.sequencer.offline_mode = True
            action_list = self._format_text(sentence)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()
            self._check_hid_reports(action_list)
        # end for
    # end def test_typing_complex_text

    def test_typing_buffered_text(self):
        """
        Check that a buffered complex text could be converted into instructions and played by the emulator.
        """
        text = ['"You never really understand a person until you consider things from his point of view.\n',
                'Until you climb inside of his skin and walk around in it" \nTo Kill a Mockingbird by Harper Lee.\n']
        self.kosmos.sequencer.offline_mode = True
        action_list = []
        for sentence in text:
            action_list.extend(self._format_text(sentence))
        # end for
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        self._check_hid_reports(action_list)
    # end def test_typing_buffered_text

    def test_minimum_pulse_duration(self):
        """
        Validate keystroke() minimum duration parameter.
        """
        start = 2000  # us
        step = 100  # us
        self.kosmos.sequencer.offline_mode = True
        for pulse_width in range(start, 0, -step):
            self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_A, duration=pulse_width / 10 ** 6)
        # end for
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        # end for
    # end def test_minimum_pulse_duration

    def test_repetitive_short_pulse(self):
        """
        Validate keystroke() minimum duration and delay parameters with repetition.
        """
        make_pulse_width = 100  # us
        break_pulse_width = 500  # us
        self.kosmos.sequencer.offline_mode = True
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_A, duration=make_pulse_width / 10 ** 6, repeat=5,
                                delay=break_pulse_width / 10**6)
        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
        # end for
    # end def test_repetitive_short_pulse

    def test_cohabitation_slider_emulator(self):
        """
        Check the KeyMatrix emulator could be used with the slider emulator.
        """
        self.slider_emulator = KosmosPowerSliderEmulator(kosmos=self.kosmos, fw_id='RBK68')
        self.kosmos.sequencer.offline_mode = True

        # Power off the DUT
        self.slider_emulator.open_slider(slider_id=0)

        self._kbd_emu.perform_action_list(action_list=[(KEY_ID.KEYBOARD_A, MAKE)], delay=.2)

        # Power on the DUT
        self.slider_emulator.close_slider(slider_id=0)

        action_list = [(KEY_ID.KEYBOARD_B, MAKE), (KEY_ID.KEYBOARD_A, BREAK),
                       (KEY_ID.KEYBOARD_C, KEYSTROKE), (KEY_ID.KEYBOARD_B, BREAK)]
        self._kbd_emu.perform_action_list(action_list=action_list, delay=.2)

        self.kosmos.sequencer.offline_mode = False
        self.kosmos.sequencer.play_sequence()
    # end def test_cohabitation_slider_emulator

    def test_release_all(self):
        """
        Validate release_all() method
        """
        # The following should print a upper-case A letter
        self._kbd_emu.key_press(key_id=KEY_ID.KEYBOARD_LEFT_SHIFT)  # expect the SHIFT key to be released by the reset
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_A)

        # Reset the keymatrix (release any pressed keys)
        self._kbd_emu.release_all()

        # Check the following prints a lower-case A letter
        self._kbd_emu.keystroke(key_id=KEY_ID.KEYBOARD_A)
    # end def test_release_all

    def _check_hid_reports(self, action_list):
        """
        Check if the key is listed in the key to HID table.

        :param action_list: list of key id and action type
        :type action_list: ``list[tuple]``

        :raise ``AssertionError``: if a key is not found in ``HidData.KEY_ID_TO_HID_MAP``
        """
        for (key, action) in action_list:
            expected_report = None
            # Button stimuli emulator uses first available variant
            variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key]))
            if action in [MAKE, KEYSTROKE]:
                expected_report = HidData.KEY_ID_TO_HID_MAP[key][variant][MAKE]
            # end if
            if action in [BREAK, KEYSTROKE]:
                expected_report = HidData.KEY_ID_TO_HID_MAP[key][variant][BREAK]
            # end if
            assert expected_report is not None, f'key {key} not found in HidData.KEY_ID_TO_HID_MAP'
        # end for
    # end def _check_hid_reports

# end class KosmosHybridKeyMatrixEmulatorTestCase


# ------------------------------------------------------------------------------
# main
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
    Entry point of the Unit Test class.
    """
    from unittest import main
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
