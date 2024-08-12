#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.slideremulator
:brief: Kosmos Slider Emulator Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/03/26
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from typing import Iterable

from pylibrary.emulator.emulatorinterfaces import SliderEmulationInterface
from pyraspi.services.kosmos.kosmosio import KosmosIO
from pyraspi.services.kosmos.protocol.generated.messages import bas_entry_t
from pyraspi.services.kosmos.protocol.generated.messages import bas_sliders_entry_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosSliderEmulator(SliderEmulationInterface):
    """
    Slider emulator leveraging Kosmos
    """

    class STATE:
        """
        Slider State [2bits] targeted switch state
        """
        NO_CONTACT = 0
        NORMALLY_CONNECTED = 1  # i.e. normally closed
        DISCONNECTED = 2  # i.e. normally open
        NO_CONTACT_2 = 3
    # end class STATE

    class KEY:
        """
        Slider enable key
        """
        DISABLED = 0
        ENABLED = 2
    # end class KEY

    def __init__(self, kosmos):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        """
        self._kosmos = kosmos
    # end def __init__

    def open_slider(self, slider_id):
        # See ``PowerSliderEmulationInterface.open_slider``
        bas_entry = self._create_entry(slider_ids=[slider_id], state=self.STATE.DISCONNECTED)
        self.send_instructions([bas_entry])
    # end def open_slider

    def close_slider(self, slider_id):
        # See ``PowerSliderEmulationInterface.close_slider``
        bas_entry = self._create_entry(slider_ids=[slider_id], state=self.STATE.NORMALLY_CONNECTED)
        self.send_instructions([bas_entry])
    # end def close_slider

    def make_before_break(self, slider_id):
        # See ``PowerSliderEmulationInterface.make_before_break``
        bas_entry = self._create_entry(slider_ids=[slider_id], state=self.STATE.NO_CONTACT)

        self.send_instructions([bas_entry])
    # end def make_before_break

    def no_contact_2(self, slider_id):
        # See ``PowerSliderEmulationInterface.no_contact_2``
        bas_entry = self._create_entry(slider_ids=[slider_id], state=self.STATE.NO_CONTACT_2)

        self.send_instructions([bas_entry])
    # end def no_contact_2

    def _create_entry(self, slider_ids, state):
        """
        Configure the slider state on the given slider identifiers

        :param slider_ids: List of Slider identifiers
        :type slider_ids: ``list[KosmosIO.SLIDERS]``
        :param state: Slider state
        :type state: ``STATE``

        :return: Slider instructions with the new state
        :rtype: ``bas_entry_t``

        :raise ``AssertionError``: If a slider identifier is not in its valid range
        """
        all_slider_ids = []
        for slider_id in slider_ids:
            if isinstance(slider_id, Iterable):
                for sub_slider_id in slider_id:
                    assert sub_slider_id in KosmosIO.SLIDERS, (slider_ids, slider_id, sub_slider_id)
                    all_slider_ids.append(sub_slider_id)
                # end for
            else:
                assert slider_id in KosmosIO.SLIDERS, (slider_ids, slider_id)
                all_slider_ids.append(slider_id)
            # end if
        # end for

        slider_entry = bas_sliders_entry_t()
        if KosmosIO.SLIDERS.SLIDER_0 in all_slider_ids:
            slider_entry.bit.slider_0_state = state
            slider_entry.bit.slider_0_enable = self.KEY.ENABLED
        # end if
        if KosmosIO.SLIDERS.SLIDER_1 in all_slider_ids:
            slider_entry.bit.slider_1_state = state
            slider_entry.bit.slider_1_enable = self.KEY.ENABLED
        # end if
        if KosmosIO.SLIDERS.SLIDER_2 in all_slider_ids:
            slider_entry.bit.slider_2_state = state
            slider_entry.bit.slider_2_enable = self.KEY.ENABLED
        # end if
        if KosmosIO.SLIDERS.SLIDER_3 in all_slider_ids:
            slider_entry.bit.slider_3_state = state
            slider_entry.bit.slider_3_enable = self.KEY.ENABLED
        # end if

        bas_entry = bas_entry_t()
        bas_entry.bloc.sliders = slider_entry
        return bas_entry
    # end def _create_entry

    def send_instructions(self, entries, delay=None):
        """
        Add a list of Slider entry plus EXECUTE instructions in the global buffer then send the Go signal to the Kosmos
        board

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
# end class KosmosSliderEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
