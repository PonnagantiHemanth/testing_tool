#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.basicbuttonemulator
:brief: Raspi Button Control Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/03/09
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep
from warnings import warn

from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.emulatorinterfaces import Rpi4ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.raspi import Raspi
from pyraspi.services.daemon import Daemon

if Raspi.is_host_raspberry_pi():
    import RPi.GPIO as GPIO
# end if


# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
if not Daemon.is_host_kosmos():
    KEY_ID_TO_GPIO_TABLE = {
        KEY_ID.LEFT_BUTTON: Raspi.PIN.LEFT_BUTTON,
        KEY_ID.RIGHT_BUTTON: Raspi.PIN.RIGHT_BUTTON,
        KEY_ID.MIDDLE_BUTTON: Raspi.PIN.MIDDLE_BUTTON,
        KEY_ID.FORWARD_BUTTON: Raspi.PIN.FORWARD,
        KEY_ID.BACK_BUTTON: Raspi.PIN.BACK,
        KEY_ID.CONNECT_BUTTON: Raspi.PIN.EASY_SWITCH_BUTTON,
        KEY_ID.DPI_CYCLING_BUTTON: Raspi.PIN.DPI_CYCLING_BUTTON,
        KEY_ID.DPI_UP_BUTTON: Raspi.PIN.DPI_UP_BUTTON,
        KEY_ID.DPI_DOWN_BUTTON: Raspi.PIN.DPI_DOWN_BUTTON,
        KEY_ID.DPI_SHIFT_BUTTON: Raspi.PIN.DPI_SHIFT_BUTTON,
        KEY_ID.CYCLE_THROUGH_ONBOARD_PROFILE: Raspi.PIN.CYCLE_THROUGH_ONBOARD_PROFILE,
        KEY_ID.EMOJI_PANEL: Raspi.PIN.EMOJI_PANEL,
        KEY_ID.SMART_SHIFT: Raspi.PIN.SMART_SHIFT,
        KEY_ID.BUTTON_1: Raspi.PIN.BUTTON_1,
        KEY_ID.BUTTON_2: Raspi.PIN.BUTTON_2,
        KEY_ID.BUTTON_3: Raspi.PIN.BUTTON_3,
        KEY_ID.BUTTON_4: Raspi.PIN.BUTTON_4,
        KEY_ID.BUTTON_5: Raspi.PIN.BUTTON_5,
        KEY_ID.BUTTON_6: Raspi.PIN.BUTTON_6,
        KEY_ID.BUTTON_7: Raspi.PIN.BUTTON_7,
        KEY_ID.BUTTON_8: Raspi.PIN.BUTTON_8,
        KEY_ID.BUTTON_9: Raspi.PIN.BUTTON_9,
        KEY_ID.BUTTON_10: Raspi.PIN.BUTTON_10,
        KEY_ID.BUTTON_11: Raspi.PIN.BUTTON_11,
        KEY_ID.BUTTON_12: Raspi.PIN.BUTTON_12,
        KEY_ID.BUTTON_13: Raspi.PIN.BUTTON_13,
        KEY_ID.BUTTON_14: Raspi.PIN.BUTTON_14,
        KEY_ID.BUTTON_15: Raspi.PIN.BUTTON_15,
        KEY_ID.BUTTON_16: Raspi.PIN.BUTTON_16,
    }
# end if

HOST_INDEX_TO_KEY_ID_MAP = {
    HOST.CH1: KEY_ID.CONNECT_BUTTON,
    HOST.CH2: KEY_ID.CONNECT_BUTTON,
    HOST.CH3: KEY_ID.CONNECT_BUTTON,
}


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BasicButtonEmulator(Rpi4ButtonStimuliInterface):
    """
    ButtonEmulator Control Class, directly controlled by the Raspberry Pi GPIOs.
    """
    def __init__(self, verbose=False):
        """
        :param verbose: To enable the debug message or not, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: If Raspberry Pi host is incompatible with this class
        """
        # GPIO can be setup only if host is a RaspberryPi, but not configured for Kosmos project
        assert Raspi.is_host_raspberry_pi() and not Daemon.is_host_kosmos(),\
            f'GPIO can be setup only if host is a RaspberryPi, but not configured for Kosmos project.'

        self.verbose = verbose
        self.connected_key_ids = None

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        self.keyword_key_ids = {
            "user_action": KEY_ID.LEFT_BUTTON,
            "enter_dfu_action": KEY_ID.BUTTON_5  # Lexend
        }
    # end def __init__

    @property
    def passive_hold_press_support(self):
        # See ``ButtonStimuliInterface.passive_hold_press_support``
        return True
    # end def passive_hold_press_support

    def __del__(self):
        """
        Cleanup GPIO
        """
        if Raspi.is_host_raspberry_pi() and not Daemon.is_host_kosmos():
            GPIO.cleanup(list(KEY_ID_TO_GPIO_TABLE.values()))
        # end if
    # end def __del__

    def setup_connected_key_ids(self):
        # See ``ButtonStimuliInterface.setup_connected_key_ids``
        connected_key_ids = []
        key_ids = list(KEY_ID_TO_GPIO_TABLE.keys())
        gpios = list(KEY_ID_TO_GPIO_TABLE.values())
        for index, pin in enumerate(gpios):
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            if GPIO.input(pin) != GPIO.LOW:
                connected_key_ids.append(key_ids[index])
            # end if
            GPIO.cleanup(pin)
        # end for
        self.connected_key_ids = connected_key_ids
        if self.verbose:
            print(f'Connected key Ids: {connected_key_ids}')
        # end if
    # end def setup_connected_key_ids

    def release_all(self):
        # See ``ButtonStimuliInterface.release_all``
        # Release all the buttons
        for pin in list(KEY_ID_TO_GPIO_TABLE.values()):
            GPIO.cleanup(pin)
        # end for
    # end def release_all

    def left_click(self, duration=0.2):
        """
        Emulate a left button click.

        :param duration: delay between make and break, defaults to 0.2 second - OPTIONAL
        :type duration: ``int``
        """
        self.keystroke(KEY_ID.LEFT_BUTTON, duration=duration)
    # end def left_click

    def change_host(self, host_index=HOST.CH1, delay=2):
        # See ``ButtonStimuliInterface.change_host``
        if host_index in HOST.ALL:
            self.keystroke(HOST_INDEX_TO_KEY_ID_MAP[host_index], delay=delay)
        else:
            warn(f'Unsupported host index: {host_index}')
        # end if
    # end def change_host

    def enter_pairing_mode(self, host_index=HOST.CH1, delay=2):
        # See ``ButtonStimuliInterface.enter_pairing_mode``
        if host_index in HOST.ALL:
            self.keystroke(HOST_INDEX_TO_KEY_ID_MAP[host_index], duration=3.2, delay=delay)
        else:
            warn(f'Unsupported host index: {host_index}')
        # end if
    # end def enter_pairing_mode

    def keystroke(self, key_id, duration=.12, repeat=1, delay=.05):
        # See ``ButtonStimuliInterface.keystroke``
        for _ in range(repeat):
            self.key_press(key_id)
            sleep(duration)
            self.key_release(key_id)
            if delay:
                sleep(delay)
            # end if
        # end for
    # end def keystroke

    def simultaneous_keystroke(self, key_ids, duration=0.3):
        """
        Emulate simultaneous keystrokes.

        :param key_ids: List of unique identifier of the keys to emulate
        :type key_ids: ``list[KEY_ID or int]``
        :param duration: delay between make and break, defaults to 0.3 second - OPTIONAL
        :type duration: ``float``
        """
        self.multiple_keys_press(key_ids)
        sleep(duration)
        self.multiple_keys_release(key_ids)
    # end def simultaneous_keystroke

    def key_press(self, key_id):
        # See ``ButtonStimuliInterface.key_press``
        if self.key_ids_check(key_id):
            warn(f'Unsupported key id: {key_id}')
        elif self.connected_key_ids and key_id not in self.connected_key_ids:
            warn(f'Pin {KEY_ID_TO_GPIO_TABLE[key_id]} may not be connected')
        else:
            GPIO.setup(KEY_ID_TO_GPIO_TABLE[key_id], GPIO.OUT, initial=GPIO.LOW)
        # end if
    # end def key_press

    def key_release(self, key_id):
        # See ``ButtonStimuliInterface.key_release``
        if self.key_ids_check(key_id):
            warn(f'Unsupported key id: {key_id}')
        elif self.connected_key_ids and key_id not in self.connected_key_ids:
            warn(f'Pin {KEY_ID_TO_GPIO_TABLE[key_id]} may not be connected')
        else:
            GPIO.cleanup(KEY_ID_TO_GPIO_TABLE[key_id])
        # end if
    # end def key_release

    def key_ids_check(self, key_ids):
        """
        Check key ids support

        :param key_ids: List of unique identifier of the keys to check
        :type key_ids: ``list[KEY_ID or int]``

        :return: List of errors, empty list if no error
        :rtype: ``list[tuple[int, int]]``
        """
        if not isinstance(key_ids, list):
            key_ids = [key_ids]
        # end if
        unsupported_key = 1
        pin_not_connected = 2
        error = []

        for key_id in key_ids:
            if key_id not in KEY_ID_TO_GPIO_TABLE.keys() or KEY_ID_TO_GPIO_TABLE[key_id] is None:
                warn(f'Unsupported key id: {str(key_id)}')
                error.append((key_id, unsupported_key))
            # end if
            if self.connected_key_ids and (key_id not in self.connected_key_ids):
                warn(f'Pin {str(KEY_ID_TO_GPIO_TABLE[key_id])} may not be connected')
                error.append((key_id, pin_not_connected))
            # end if
        # end for
        return error
    # end def key_ids_check

    def multiple_keys_press(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_press``
        if self.key_ids_check(key_ids):
            warn(f'Unsupported key id: {key_ids}')
            return
        # end if

        # First loop to setup only, to be as fast as possible
        for key_id in key_ids:
            GPIO.setup(KEY_ID_TO_GPIO_TABLE[key_id], GPIO.OUT, initial=GPIO.LOW)
            if delay is not None:
                sleep(delay)
            # end if
        # end for
    # end def multiple_keys_press

    def multiple_keys_release(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_release``
        if self.key_ids_check(key_ids):
            warn(f'Unsupported key id: {key_ids}')
            return
        # end if

        for key_id in key_ids:
            gpio = KEY_ID_TO_GPIO_TABLE[key_id]
            GPIO.cleanup(gpio)
            if delay is not None:
                sleep(delay)
            # end if
        # end for
    # end def multiple_keys_release

    def get_key_id_list(self):
        # See ``ButtonStimuliInterface.get_key_id_list``
        return self.connected_key_ids
    # end def get_key_id_list

    def get_hybrid_key_id_list(self):
        # See ``ButtonStimuliInterface.get_hybrid_key_id_list``
        return []
    # end def get_hybrid_key_id_list

    def get_fn_keys(self):
        # See ``ButtonStimuliInterface.get_fn_keys``
        return {}
    # end def get_fn_keys

    def get_key_id_to_gpio_table(self):
        # See ``ButtonStimuliInterface.get_key_id_to_gpio_table``
        return KEY_ID_TO_GPIO_TABLE
    # end def get_key_id_to_gpio_table

    def user_action(self):
        # See ``ButtonStimuliInterface.user_action``
        self.keystroke(self.keyword_key_ids["user_action"])
    # end def user_action
# end class BasicButtonEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
