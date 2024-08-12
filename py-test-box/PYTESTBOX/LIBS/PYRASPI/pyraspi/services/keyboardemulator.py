#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyraspi.services.keyboardmulator
    :brief: Raspi4 Keyboard Emulator Class
    :author: Fred Chen <fchen7@logitech.com>
    :date: 2021/02/01
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import abc
from enum import IntEnum
from enum import unique
from sys import stdout
from time import sleep

from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import KEYSTROKE
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.emulatorinterfaces import Rpi4ButtonStimuliInterface
from pylibrary.emulator.keybaordlayout import KbdMatrix
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.raspi import Raspi
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.config.keybaordlayout import GET_KEYBOARD_LAYOUT_BY_ID
from pyraspi.services.mt8816 import MT8816

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
HOST_INDEX_TO_KEY_ID_MAP = {
    HOST.CH1: KEY_ID.HOST_1,
    HOST.CH2: KEY_ID.HOST_2,
    HOST.CH3: KEY_ID.HOST_3,
}


NUMBER_TO_KEYBOARD_KEY_ID_MAP = {
    0: KEY_ID.KEYBOARD_0,
    1: KEY_ID.KEYBOARD_1,
    2: KEY_ID.KEYBOARD_2,
    3: KEY_ID.KEYBOARD_3,
    4: KEY_ID.KEYBOARD_4,
    5: KEY_ID.KEYBOARD_5,
    6: KEY_ID.KEYBOARD_6,
    7: KEY_ID.KEYBOARD_7,
    8: KEY_ID.KEYBOARD_8,
    9: KEY_ID.KEYBOARD_9,
}


@unique
class KeyState(IntEnum):
    """
    Key state.
    """
    BREAK = 0  # synonyms: OFF, Released, False
    MAKE = 1   # synonyms: ON, Pressed, True
# end class KeyState


class KeyboardMixin(ButtonStimuliInterface, metaclass=abc.ABCMeta):
    """
    Common implementation class for Keyboard emulators.
    """
    class LAYOUT:
        """
        Define the type of keyboard layout
        cf kbdm_layoutKey_ts in kdb_map.h
        """
        DEFAULT = 0
        ANSI = DEFAULT
        # The conversion method between keyboard international layouts and physical layouts could be found here:
        # pytestbox.device.base.layoututils.LayoutTestUtils.select_layout
        ISO_104_KEY = 1
        ISO_105_KEY = 2
        ISO_107_KEY = 3
        JIS_109_KEY = 4
        MAX = JIS_109_KEY

        @classmethod
        def get_string_name(cls, layout_index):
            """
            Get the string name of the specific layout index

            :param layout_index: Index of the international layout
            :type layout_index: ``KeyboardMixin.LAYOUT | int ``

            :return: The string name of the layout index
            :rtype: ``str``

            :raise ``ValueError``: If the layout_index is unknown
            """
            if layout_index in [cls.DEFAULT, cls.ISO_104_KEY]:
                return 'ISO_104_KEY'
            elif layout_index == cls.ISO_105_KEY:
                return 'ISO_105_KEY'
            elif layout_index == cls.ISO_107_KEY:
                return 'ISO_107_KEY'
            elif layout_index == cls.JIS_109_KEY:
                return 'JIS_109_KEY'
            else:
                raise ValueError(f'Unknown layout index: {layout_index}')
            # end if
        # end def get_string_name
    # end class LAYOUT

    @abc.abstractmethod
    def __init__(self, fw_id, verbose=False):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: If the firmware identifier is not in its valid range
        """
        assert fw_id in GET_KEYBOARD_LAYOUT_BY_ID, f'Don\'t support the fw_id : {fw_id}'
        self._keyboard_layouts = GET_KEYBOARD_LAYOUT_BY_ID[fw_id]
        self._keyboard_layout = self._keyboard_layouts[self.LAYOUT.DEFAULT]

        self.connected_key_ids = None
        self.keyword_key_ids = {
            "user_action": KEY_ID.KEYBOARD_RETURN_ENTER
        }
        self._host = None
        self._is_pairing = False

        self.fn_pressed = False
        self.fn_locked = False

        self.verbose = verbose
    # end def __init__

    def _sleep(self, delay):
        """
        Implementation specific sleep instruction. Can be overloaded by derived classes.

        :param delay: Delay command, in second
        :type delay: ``float``
        """
        if delay is not None and delay > 0:
            sleep(delay)
        # end if
    # end def _sleep

    @property
    def passive_hold_press_support(self):
        # See ``ButtonStimuliInterface.passive_hold_press_support``
        return True
    # end def passive_hold_press_support

    @property
    def keyboard_layout(self):
        """
        Get the selected physical keyboard layout.

        :return: The physical keyboard layout which was configured
        :rtype: ``CommonKeyMatrix``
        """
        return self._keyboard_layout
    # end def keyboard_layout

    def setup_connected_key_ids(self):
        # See ``ButtonStimuliInterface.setup_connected_key_ids``
        self.connected_key_ids = list(self._keyboard_layout.KEYS.keys()) + list(self._keyboard_layout.FN_KEYS.keys())
    # end def setup_connected_key_ids

    def change_host(self, host_index=None, delay=2):
        # See ``ButtonStimuliInterface.change_host``
        self._validate_input_and_update_host_index(host_index, change_host_cycling=True)
        if self.verbose:
            stdout.write(f'change host: input host: {host_index}, actual host: {self._host}\n')
        # end if
        self.keystroke(key_id=HOST_INDEX_TO_KEY_ID_MAP[self._host], duration=0.1, delay=delay)
        self._is_pairing = False
    # end def change_host

    def enter_pairing_mode(self, host_index=None, delay=2):
        # See ``ButtonStimuliInterface.enter_pairing_mode``
        self._validate_input_and_update_host_index(host=host_index, change_host_cycling=False)
        if self.verbose:
            stdout.write(f'enter pairing mode: input host: {host_index}, actual host: {self._host}\n')
        # end if
        self.keystroke(key_id=HOST_INDEX_TO_KEY_ID_MAP[self._host], duration=3.2, delay=delay)
        self._is_pairing = True
    # end def enter_pairing_mode

    def perform_fn_lock_key_combination(self, is_gaming):
        """
        Perform fn lock key combination

        :param is_gaming: Flag indicating if the DUT is a gaming or a C&P product
        :type is_gaming: ``bool``
        """
        if self.verbose:
            stdout.write(f'perform fn lock key combination')
        # end if

        if is_gaming:
            # Gaming keyboard
            self.keystroke(KEY_ID.FN_KEY)
        else:
            # C&P keyboard
            fn_lock_key_combination = [KEY_ID.FN_KEY, KEY_ID.KEYBOARD_ESCAPE]
            self.multiple_keys_press(fn_lock_key_combination,
                                     delay=ButtonStimuliInterface.DEFAULT_DELAY)
            sleep(ButtonStimuliInterface.DEFAULT_DURATION)
            self.multiple_keys_release(fn_lock_key_combination)
            sleep(ButtonStimuliInterface.DEFAULT_DURATION)
        # end if
    # end def perform_fn_lock_key_combination

    def keystroke(self, key_id, duration=.1, repeat=1, delay=.05):
        # See ``ButtonStimuliInterface.keystroke``
        assert key_id in self._keyboard_layout.KEYS, f"The Keyboard emulator doesn't support the key : {repr(key_id)}"

        if self.verbose:
            stdout.write(f'keystroke: {str(key_id)}\n')
        # end if

        for _ in range(repeat):
            self._set_key_state(key_id, state=KeyState.MAKE)
            self._sleep(duration)
            self._set_key_state(key_id, state=KeyState.BREAK)
            self._sleep(delay)
        # end for
    # end def keystroke

    def simultaneous_keystroke(self, key_ids, duration=0.3):
        # See ``ButtonStimuliInterface.simultaneous_keystroke``
        self.multiple_keys_press(key_ids)
        self._sleep(duration)
        self.multiple_keys_release(key_ids)
    # end def simultaneous_keystroke

    def key_press(self, key_id):
        # See ``ButtonStimuliInterface.key_press``
        if self.verbose:
            stdout.write(f'key press {key_id!r}\n')
        # end if
        self._set_key_state(key_id, state=KeyState.MAKE)
    # end def key_press

    def key_release(self, key_id):
        # See ``ButtonStimuliInterface.key_release``
        if self.verbose:
            stdout.write(f'key release {key_id!r}\n')
        # end if
        self._set_key_state(key_id, state=KeyState.BREAK)
    # end def key_release

    def multiple_keys_press(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_press``
        for key_id in key_ids:
            if self.verbose:
                stdout.write(f'm key pressed: {str(key_id)}\n')
            # end if
            self._set_key_state(key_id, state=KeyState.MAKE)
            self._sleep(delay)
        # end for
    # end def multiple_keys_press

    def multiple_keys_release(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_release``
        for key_id in key_ids:
            if self.verbose:
                stdout.write(f'm key released: {str(key_id)}\n')
            # end if
            self._set_key_state(key_id, state=KeyState.BREAK)
            self._sleep(delay)
        # end for
    # end def multiple_keys_release

    def get_key_id_list(self):
        # See ``ButtonStimuliInterface.get_key_id_list``
        return self._keyboard_layout.KEYS.keys()
    # end def get_key_id_list

    def get_hybrid_key_id_list(self):
        # See ``ButtonStimuliInterface.get_hybrid_key_id_list``
        return []
    # end def get_hybrid_key_id_list

    def get_fn_keys(self):
        # See ``ButtonStimuliInterface.get_fn_keys``
        return self._keyboard_layout.FN_KEYS
    # end def get_fn_keys

    def user_action(self):
        # See ``ButtonStimuliInterface.user_action``
        self.keystroke(key_id=self.keyword_key_ids["user_action"])
    # end def user_action

    def perform_action_list(self, action_list, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                            delay=ButtonStimuliInterface.DEFAULT_DURATION):
        # See ``ButtonStimuliInterface.perform_action_list``
        for (key_id, action_id) in action_list:
            if action_id == MAKE:
                self.key_press(key_id)
                self._sleep(duration)
            elif action_id == BREAK:
                self.key_release(key_id)
                self._sleep(delay)
            elif action_id == KEYSTROKE:
                self.keystroke(key_id, duration=duration, delay=delay)
            else:
                raise ValueError(f'Invalid action_id received: {action_id}')
            # end if
        # end for
    # end def perform_action_list

    @abc.abstractmethod
    def _set_key_state(self, key_id, state):
        """
        Implementation-specific method for setting a key ON or OFF.

        :param key_id: The target key be set to ON or OFF
        :type key_id: ``KEY_ID``
        :param state: BREAK (off, released) or MAKE (on, pressed)
        :type state: ``KeyState``
        """
        raise NotImplementedError("users must define _set_key_state to use this base class")
    # end def _set_key_state

    def _validate_input_and_update_host_index(self, host, change_host_cycling=True):
        """
        Validate host input and update to self._host if it's valid.

        :param host: the target host, the possible values are 1, 2, 3 and None
        :type host: ``Any``
        :param change_host_cycling: change host cycling or not, defaults to True - OPTIONAL
        :type change_host_cycling: ``boolean``

        :raise ``AssertionError``: Unknown host button
        """
        assert host in [None, HOST.CH1, HOST.CH2, HOST.CH3], f'Unknown host button {host}'
        if host is not None:
            self._host = host
        else:
            # Emulate EasySwitch behaviors
            if change_host_cycling:
                if not self._is_pairing:
                    self._host = self._change_host_cycling()
                # end if
            else:
                # For enter pairing mode, the host won't be changed if set host=None
                # But if self._host = None, will use host 2 as default
                if self._host is None:
                    self._host = 2
                # end if
            # end if
        # end if
    # end def _validate_input_and_update_host_index

    def _change_host_cycling(self):
        """
        Change host by cycling sequence h1->h2->h3->h1...
        The h1 is the default host if self._host is None

        :return: the target host, the possible values are 1, 2 ,3
        :rtype: ``int``
        """
        if self._host is None or self._host == HOST.CH3:
            return HOST.CH1
        elif self._host == HOST.CH1:
            return HOST.CH2
        elif self._host == HOST.CH2:
            return HOST.CH3
        # end if
    # end def _change_host_cycling

    def select_layout(self, layout_type=LAYOUT.DEFAULT):
        """
        Change the keyboard international layout to match the device configuration in NVS

        :param layout_type: keyboard international layout type, defaults to `LAYOUT.DEFAULT` - OPTIONAL
        :type layout_type: ``LAYOUT``

        :raise ``AssertionError``: Out-of-bound Keyboard layout index
        """
        assert layout_type <= self.LAYOUT.MAX
        self._keyboard_layout = self._keyboard_layouts[layout_type]
    # end def select_layout

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
        return self.get_row_index(row=row), self.get_col_index(col=col)
    # end def get_row_col_indexes

    @staticmethod
    def get_col_index(col):
        """
        Convert a column variable from its MT8816 ADDRESS format to an integer value

        :param col: Key matrix column parameter
        :type col: ``KbdMatrix``

        :return: The column index
        :rtype: ``int``

        :raise ``ValueError``: If given an unknown col
        """
        if col == KbdMatrix.COL_0:
            col_index = 0
        elif col == KbdMatrix.COL_1:
            col_index = 1
        elif col == KbdMatrix.COL_2:
            col_index = 2
        elif col == KbdMatrix.COL_3:
            col_index = 3
        elif col == KbdMatrix.COL_4:
            col_index = 4
        elif col == KbdMatrix.COL_5:
            col_index = 5
        elif col == KbdMatrix.COL_6:
            col_index = 6
        elif col == KbdMatrix.COL_7:
            col_index = 7
        elif col == KbdMatrix.COL_8:
            col_index = 8
        elif col == KbdMatrix.COL_9:
            col_index = 9
        elif col == KbdMatrix.COL_10:
            col_index = 10
        elif col == KbdMatrix.COL_11:
            col_index = 11
        elif col == KbdMatrix.COL_12:
            col_index = 12
        elif col == KbdMatrix.COL_13:
            col_index = 13
        elif col == KbdMatrix.COL_14:
            col_index = 14
        elif col == KbdMatrix.COL_15:
            col_index = 15
        elif col == KbdMatrix.COL_16:
            col_index = 16
        elif col == KbdMatrix.COL_17:
            col_index = 17
        elif col == KbdMatrix.COL_18:
            col_index = 18
        elif col == KbdMatrix.COL_19:
            col_index = 19
        elif col == KbdMatrix.COL_20:
            col_index = 20
        elif col == KbdMatrix.COL_21:
            col_index = 21
        elif col == KbdMatrix.COL_22:
            col_index = 22
        elif col == KbdMatrix.COL_23:
            col_index = 23
        else:
            raise ValueError(f'Unknown col: {col}')
        # end if
        return col_index
    # end def get_col_index

    @staticmethod
    def get_row_index(row):
        """
        Convert a row variable from its MT8816 ADDRESS format to an integer value

        :param row: Key matrix row parameter
        :type row: ``KbdMatrix``

        :return: The row index
        :rtype: ``int``

        :raise ``ValueError``: If given an unknown row
        """
        if row == KbdMatrix.ROW_0:
            row_index = 0
        elif row == KbdMatrix.ROW_1:
            row_index = 1
        elif row == KbdMatrix.ROW_2:
            row_index = 2
        elif row == KbdMatrix.ROW_3:
            row_index = 3
        elif row == KbdMatrix.ROW_4:
            row_index = 4
        elif row == KbdMatrix.ROW_5:
            row_index = 5
        elif row == KbdMatrix.ROW_6:
            row_index = 6
        elif row == KbdMatrix.ROW_7:
            row_index = 7
        elif row == KbdMatrix.ROW_8:
            row_index = 8
        elif row == KbdMatrix.ROW_9:
            row_index = 9
        elif row == KbdMatrix.ROW_10:
            row_index = 10
        elif row == KbdMatrix.ROW_11:
            row_index = 11
        elif row == KbdMatrix.ROW_12:
            row_index = 12
        elif row == KbdMatrix.ROW_13:
            row_index = 13
        elif row == KbdMatrix.ROW_14:
            row_index = 14
        elif row == KbdMatrix.ROW_15:
            row_index = 15
        else:
            raise ValueError(f'Unknown row: {row}')
        # end if
        return row_index
    # end def get_row_index
# end class KeyboardMixin


class KeyboardEmulator(KeyboardMixin, Rpi4ButtonStimuliInterface):
    """
    Keyboard emulator by Matrix Control Board (i.e. Sodom or Noah), which is controlled by the Raspberry Pi GPIO bus.
    cf https://docs.google.com/document/d/1u0CHCYXi6D-9VOa_CHiaYuMyv441FzzV7HR-9-kQw3A/edit
    """

    def __init__(self, fw_id, verbose=False):
        """
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: If Raspberry Pi host is incompatible with this class
        """
        # GPIO can be setup only if host is a RaspberryPi, but not configured for Kosmos project
        assert Raspi.is_host_raspberry_pi() and not Daemon.is_host_kosmos(),\
            f'GPIO can be setup only if host is a RaspberryPi, but not configured for Kosmos project.'

        super().__init__(fw_id=fw_id, verbose=verbose)

        self.mt8816 = MT8816()
    # end def __init__

    def get_key_id_to_gpio_table(self):
        # See ``ButtonStimuliInterface.get_key_id_to_gpio_table``
        return self._keyboard_layout.KEYS
    # end def get_key_id_to_gpio_table

    def _set_key_state(self, key_id, state):
        """
        Change the state to ON or OFF for MT8816 row and column intersection

        :param key_id: The target key be set to ON or OFF
        :type key_id: ``KEY_ID``
        :param state: BREAK (off, released) or MAKE (on, pressed)
        :type state: ``KeyState``
        """
        cs, col = self._keyboard_layout.KEYS[key_id][0]
        row = self._keyboard_layout.KEYS[key_id][1]
        state_mt = MT8816.INTERSECTION.OFF if state == KeyState.BREAK else MT8816.INTERSECTION.ON
        self.mt8816.set_address(cs_pin=cs, data_pin=self.mt8816.get_data_pin(cs), x=row, y=col, state=state_mt)

        if self.verbose:
            stdout.write(f'  {state.name:5s} {KEY_ID(key_id).name}: row={row}, col={col}, cs={cs}\n')
        # end if

        if self.fn_pressed and state == KeyState.MAKE and key_id == KEY_ID.KEYBOARD_ESCAPE:
            # C&P: Toggle Fn-Lock with the Fn-ESC command. Note that this class could not handle G products
            self.fn_locked = not self.fn_locked
        elif key_id in [KEY_ID.FN_KEY, KEY_ID.R_FN_KEY]:
            self.fn_pressed = (state == KeyState.MAKE)
        # end if
    # end def _set_key_state

    def release_all(self):
        # See ``ButtonStimuliInterface.release_all``
        if self.verbose:
            stdout.write('reset mt8816\n')
        # end if
        self.mt8816.reset()
    # end def release_all
# end class KeyboardEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
