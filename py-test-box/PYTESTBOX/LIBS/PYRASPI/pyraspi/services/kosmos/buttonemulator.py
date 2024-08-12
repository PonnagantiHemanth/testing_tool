#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.buttonemulator
:brief: Kosmos Button Emulator Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import unique
from typing import Iterable

from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pyraspi.services.daemon import Daemon
from pyraspi.services.kosmos.config.buttonlayout import BUTTON_LAYOUT_BY_ID
from pyraspi.services.kosmos.kosmosio import KosmosIO
from pyraspi.services.kosmos.protocol.generated.messages import bas_buttons_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import bas_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import bas_sliders_entry_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosButtonEmulator(ButtonStimuliInterface):
    """
    Button emulator leveraging Kosmos. Button action can be emulated by switches or sliders Kosmos hardware
    """

    @unique
    class BUTTON_STATE(IntEnum):
        """
        Button State [1bit] targeted button state
        Warning: we could not use auto() here as the value is used to configure a bas_buttons_entry_t object !
        """
        OFF = 0
        ON = 1
    # end class BUTTON_STATE

    @unique
    class BUTTON_KEY(IntEnum):
        """
        Button enable key
        Warning: we could not use auto() here as the value is used to configure a bas_buttons_entry_t object !
        """
        DISABLED = 0
        ENABLED = 1
    # end class BUTTON_KEY

    class SLIDER_STATE:
        """
        Slider State [2bits] targeted switch state
        """
        NO_CONTACT = 0
        NORMALLY_CONNECTED = 1  # i.e. normally closed
        NORMALLY_DISCONNECTED = 2  # i.e. normally open
        NO_CONTACT_2 = 3
    # end class SLIDER_STATE

    class SLIDER_KEY:
        """
        Slider enable key
        """
        DISABLED = 0
        ENABLED = 2
    # end class SLIDER_KEY

    def __init__(self, kosmos, fw_id, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: Flag enabling the verbosity level, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: This class can only be instantiated on a Kosmos hardware
        """
        assert Daemon.is_host_kosmos(), 'This class supports only Kosmos hardware'

        assert fw_id in BUTTON_LAYOUT_BY_ID, f'Don\'t support the fw_id : {fw_id}'
        self._button_layout = BUTTON_LAYOUT_BY_ID[fw_id]
        self.connected_key_ids = None

        self._kosmos = kosmos
        self.verbose = verbose

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

    def setup_connected_key_ids(self):
        # See ``ButtonStimuliInterface.setup_connected_key_ids``
        self.connected_key_ids = self._button_layout.KEYS.keys()
    # end def setup_connected_key_ids

    def release_all(self):
        # See ``ButtonStimuliInterface.release_all``
        # Generate the RELEASE on all supported buttons
        bas_entry = self._create_entry(bas_ids=list(self._button_layout.KEYS.values()), state=self.BUTTON_STATE.OFF)
        self.send_instructions([bas_entry])
    # end def release_all

    def change_host(self, host_index=None, delay=None):
        # See ``ButtonStimuliInterface.change_host``
        self.keystroke(key_id=KEY_ID.CONNECT_BUTTON, duration=0.1)
    # end def change_host

    def enter_pairing_mode(self, host_index=None, delay=None):
        # See ``ButtonStimuliInterface.enter_pairing_mode``
        self.keystroke(key_id=KEY_ID.CONNECT_BUTTON, duration=3.2)
    # end def enter_pairing_mode

    def keystroke(self, key_id, duration=ButtonStimuliInterface.DEFAULT_DURATION, repeat=1,
                  delay=ButtonStimuliInterface.DEFAULT_DELAY):
        # See ``ButtonStimuliInterface.keystroke``
        assert key_id in self._button_layout.KEYS, f'The Button emulator don\'t support the key : {repr(key_id)}'
        assert duration is not None or duration == 0, f'Wrong duration parameter, got {duration}'

        if self.verbose:
            print(f'keystroke: {key_id}')
        # end if

        for _ in range(repeat):
            # Generate the MAKE user action
            bas_entry = self._create_entry(bas_ids=[self._button_layout.KEYS[key_id]], state=self.BUTTON_STATE.ON)
            # Add the button entry into the instruction buffer
            self._kosmos.bas.append(bas_entry)
            # Create an EXECUTE instruction to trigger the MAKE event
            self._kosmos.pes.execute(action=self._kosmos.bas.action_event.SEND)

            # Create a DELAY event to manage the duration of the make and trigger the release
            self._kosmos.pes.delay(delay_s=duration, action=self._kosmos.bas.action_event.SEND)

            # Generate the RELEASE user action
            bas_entry = self._create_entry(bas_ids=[self._button_layout.KEYS[key_id]], state=self.BUTTON_STATE.OFF)
            # Add the button entry into the instruction buffer
            self._kosmos.bas.append(bas_entry)

            if delay is not None and delay > 0:
                # Create a DELAY event to prevent any other action to occur
                self._kosmos.pes.delay(delay_s=delay)
            # end if

            # Start to play the defined scenario
            self._kosmos.sequencer.play_sequence()
        # end for
    # end def keystroke

    def key_press(self, key_id):
        # See ``ButtonStimuliInterface.key_press``
        assert key_id in self._button_layout.KEYS, f'The Button emulator don\'t support the key : {repr(key_id)}'

        # Generate the MAKE user action
        bas_entry = self._create_entry(bas_ids=[self._button_layout.KEYS[key_id]], state=self.BUTTON_STATE.ON)
        self.send_instructions([bas_entry])
    # end def key_press

    def key_release(self, key_id):
        # See ``ButtonStimuliInterface.key_release``
        assert key_id in self._button_layout.KEYS, f'The Button emulator don\'t support the key : {repr(key_id)}'

        # Generate the RELEASE user action
        bas_entry = self._create_entry(bas_ids=[self._button_layout.KEYS[key_id]], state=self.BUTTON_STATE.OFF)
        self.send_instructions([bas_entry])
    # end def key_release

    def multiple_keys_press(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_press``
        if delay is None:
            # Generate the MAKE user action on all given KEY_IDs at once
            bas_entry_list = [self._create_entry(bas_ids=[self._button_layout.KEYS[x] for x in key_ids],
                                                 state=self.BUTTON_STATE.ON)]
        else:
            bas_entry_list = []
            for key_id in key_ids:
                # Generate the MAKE user action on one given KEY_ID at a time
                # Note: delay instruction will be inserted after each key make by send_instructions() method
                bas_entry_list.append(
                    self._create_entry(bas_ids=[self._button_layout.KEYS[key_id]], state=self.BUTTON_STATE.ON))
            # end for
        # end if

        self.send_instructions(bas_entry_list, delay=delay)
    # end def multiple_keys_press

    def multiple_keys_release(self, key_ids, delay=None):
        # See ``ButtonStimuliInterface.multiple_keys_release``
        if delay is None:
            # Generate the RELEASE user action on all given KEY_IDs at once
            bas_entry_list = [self._create_entry(bas_ids=[self._button_layout.KEYS[x] for x in key_ids],
                                                 state=self.BUTTON_STATE.OFF)]
        else:
            bas_entry_list = []
            for key_id in key_ids:
                # Generate the RELEASE user action on one given KEY_ID at a time
                # Note: delay instruction will be inserted after each key release by send_instructions() method
                bas_entry_list.append(
                    self._create_entry(bas_ids=[self._button_layout.KEYS[key_id]], state=self.BUTTON_STATE.OFF))
            # end for
        # end if

        self.send_instructions(bas_entry_list, delay=delay)
    # end def multiple_keys_release

    def get_key_id_list(self):
        # See ``ButtonStimuliInterface.get_key_id_list``
        return self._button_layout.KEYS.keys()
    # end def get_key_id_list

    def get_hybrid_key_id_list(self):
        # See ``ButtonStimuliInterface.get_hybrid_key_id_list``
        return self._button_layout.OPTICAL_KEYS.keys() if self._button_layout.HAS_HYBRID_SWITCH else []
    # end def get_hybrid_key_id_list

    def get_fn_keys(self):
        # See ``ButtonStimuliInterface.get_fn_keys``
        return {}
    # end def get_fn_keys

    def user_action(self):
        # See ``ButtonStimuliInterface.user_action``
        self.keystroke(key_id=self.keyword_key_ids["user_action"])
    # end def user_action

    def simultaneous_keystroke(self, key_ids, duration=0.3):
        """
        Emulate simultaneous keystrokes.

        :param key_ids: List of unique identifier of the keys to emulate
        :type key_ids: ``list[KEY_ID or int]``
        :param duration: delay between make and break - OPTIONAL
        :type duration: ``float``
        """
        self.multiple_keys_press(key_ids)
        if duration is not None:
            # Create a DELAY event to manage the duration of the makes
            self._kosmos.pes.delay(delay_s=duration)
        # end if
        self.multiple_keys_release(key_ids)
    # end def simultaneous_keystroke

    def _create_entry(self, bas_ids, state):
        """
        Configure the button state on the given button identifier list

        :param bas_ids: List of button and slider identifier
        :type bas_ids: ``Iterable[KosmosIO.BUTTONS, Iterable[KosmosIO.BUTTONS]]``
        :param state: Button state
        :type state: ``KosmosButtonEmulator.BUTTON_STATE``

        :return: BAS module instruction
        :rtype: ``bas_entry_t``

        :raise ``AssertionError``: Invalid button or slider identifier
        """
        all_bas_ids = []
        for bas_id in bas_ids:
            if isinstance(bas_id, Iterable):
                for sub_bas_id in bas_id:
                    assert (sub_bas_id in KosmosIO.BUTTONS or
                            sub_bas_id in KosmosIO.SLIDERS), (bas_ids, bas_id, sub_bas_id)
                    all_bas_ids.append(sub_bas_id)
                # end for
            else:
                assert bas_id in KosmosIO.BUTTONS or bas_id in KosmosIO.SLIDERS, (bas_ids, bas_id)
                all_bas_ids.append(bas_id)
            # end if
        # end for

        # Button entry
        button_entry = bas_buttons_entry_t()
        if KosmosIO.BUTTONS.BUTTON_0 in all_bas_ids:
            button_entry.bit.button_0_state = state
            button_entry.bit.button_0_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_1 in all_bas_ids:
            button_entry.bit.button_1_state = state
            button_entry.bit.button_1_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_2 in all_bas_ids:
            button_entry.bit.button_2_state = state
            button_entry.bit.button_2_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_3 in all_bas_ids:
            button_entry.bit.button_3_state = state
            button_entry.bit.button_3_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_4 in all_bas_ids:
            button_entry.bit.button_4_state = state
            button_entry.bit.button_4_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_5 in all_bas_ids:
            button_entry.bit.button_5_state = state
            button_entry.bit.button_5_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_6 in all_bas_ids:
            button_entry.bit.button_6_state = state
            button_entry.bit.button_6_enable = self.BUTTON_KEY.ENABLED
        # end if
        if KosmosIO.BUTTONS.BUTTON_7 in all_bas_ids:
            button_entry.bit.button_7_state = state
            button_entry.bit.button_7_enable = self.BUTTON_KEY.ENABLED
        # end if

        # Slider entry
        slider_entry = bas_sliders_entry_t()
        slider_state = self.SLIDER_STATE.NORMALLY_CONNECTED if state == self.BUTTON_STATE.ON else (
            self.SLIDER_STATE.NORMALLY_DISCONNECTED)
        if KosmosIO.SLIDERS.SLIDER_0 in all_bas_ids:
            slider_entry.bit.slider_0_state = slider_state
            slider_entry.bit.slider_0_enable = self.SLIDER_KEY.ENABLED
        # end if
        if KosmosIO.SLIDERS.SLIDER_1 in all_bas_ids:
            slider_entry.bit.slider_1_state = slider_state
            slider_entry.bit.slider_1_enable = self.SLIDER_KEY.ENABLED
        # end if
        if KosmosIO.SLIDERS.SLIDER_2 in all_bas_ids:
            slider_entry.bit.slider_2_state = slider_state
            slider_entry.bit.slider_2_enable = self.SLIDER_KEY.ENABLED
        # end if
        if KosmosIO.SLIDERS.SLIDER_3 in all_bas_ids:
            slider_entry.bit.slider_3_state = slider_state
            slider_entry.bit.slider_3_enable = self.SLIDER_KEY.ENABLED
        # end if

        bas_entry = bas_entry_t()
        bas_entry.bloc.buttons = button_entry
        bas_entry.bloc.sliders = slider_entry
        return bas_entry
    # end def _create_entry

    def send_instructions(self, entries, delay=None):
        """
        Add a list of Slider entry plus EXECUTE instructions in the global buffer, then send the Go message to the
        MicroBlaze

        :param entries: Slider instructions with the new state
        :type entries: ``list[bas_entry_t]``
        :param delay: time between 2 actions - OPTIONAL
        :type delay: ``float``
        """
        for entry in entries:
            # Add the switch slider word into the instruction buffer
            self._kosmos.bas.append(entry)

            # Create an EXECUTE instruction to trigger the event
            self._kosmos.pes.execute(action=self._kosmos.bas.action_event.SEND)

            if delay is not None and delay > 0:
                # Create a DELAY event
                self._kosmos.pes.delay(delay_s=delay)
            # end if
        # end for

        # Start to play the defined scenario
        self._kosmos.sequencer.play_sequence()
    # end def send_instructions

    def perform_action_list(self, action_list, duration=ButtonStimuliInterface.DEFAULT_DURATION,
                            delay=ButtonStimuliInterface.DEFAULT_DURATION):
        # See ``ButtonStimuliInterface.perform_action_list``
        is_offline_enabled = self._kosmos.sequencer.offline_mode
        if not is_offline_enabled:
            self._kosmos.sequencer.offline_mode = True
        # end if

        super().perform_action_list(action_list=action_list, duration=duration, delay=delay)

        if not is_offline_enabled:
            self._kosmos.sequencer.offline_mode = False
            self._kosmos.sequencer.play_sequence()
        # end if
    # end def perform_action_list
# end class KosmosButtonEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
