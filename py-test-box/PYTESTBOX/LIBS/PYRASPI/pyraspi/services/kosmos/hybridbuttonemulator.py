#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.hybridbuttonemulator
:brief: Kosmos Hybrid Button Emulator Class
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2024/01/31
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import HybridButtonStimuliInterface
from pyraspi.services.kosmos.buttonemulator import KosmosButtonEmulator


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosHybridButtonEmulator(KosmosButtonEmulator, HybridButtonStimuliInterface):
    """
    Hybrid Button emulator leveraging Kosmos. Button action can be emulated by switches or sliders Kosmos hardware
    This implementation is specific for Hybrid (optical + galvanic) switches.
    """
    def __init__(self, kosmos, fw_id, verbose=False):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``
        :param verbose: Flag enabling the verbosity level, defaults to False - OPTIONAL
        :type verbose: ``bool``

        :raise ``AssertionError``: Invalid fw_id
        """
        super().__init__(kosmos=kosmos, fw_id=fw_id, verbose=verbose)
        assert self._button_layout.HAS_HYBRID_SWITCH, f"{fw_id} shall enable the hybrid switch configuration"
    # end def __init__

    def hybrid_key_press(self, key_id, galvanic_emulation=True, optical_emulation=True, galvanic_optical_delay=0):
        # See ``HybridButtonStimuliInterface.hybrid_key_press``
        assert key_id in self._button_layout.KEYS, f"The Button emulator don't support the key : {repr(key_id)}"
        assert key_id in self._button_layout.OPTICAL_KEYS, (
            f'The key : {repr(key_id)} is not configured as a hybrid switch')
        assert galvanic_emulation or optical_emulation, ("At least one of the 2 options (i.e. galvanic_emulation or "
                                                         "optical_emulation) must be True")

        bas_ids = list(self._button_layout.KEYS[key_id])
        optical_bas_id = self._button_layout.OPTICAL_KEYS[key_id]
        galvanic_bas_id = bas_ids.copy()
        galvanic_bas_id.remove(optical_bas_id)

        if galvanic_emulation and optical_emulation:
            if galvanic_optical_delay == 0:
                self.key_press(key_id=key_id)
            else:
                first_make = galvanic_bas_id if galvanic_optical_delay > 0 else optical_bas_id
                second_make = optical_bas_id if galvanic_optical_delay > 0 else galvanic_bas_id
                # Generate the MAKE user action only for the first make (optical or galvanic)
                bas_entry = self._create_entry(bas_ids=[first_make], state=self.BUTTON_STATE.ON)
                # Add the button entry into the instruction buffer
                self._kosmos.bas.append(bas_entry)
                # Create an EXECUTE instruction to trigger the MAKE event
                self._kosmos.pes.execute(action=self._kosmos.bas.action_event.SEND)
                # Create a DELAY between the make of optical and galvanic part
                self._kosmos.pes.delay(delay_s=abs(galvanic_optical_delay), action=self._kosmos.bas.action_event.SEND)
                # Generate the MAKE user action only for the second make (optical or galvanic)
                bas_entry = self._create_entry(bas_ids=[second_make], state=self.BUTTON_STATE.ON)
                # Add the button entry into the instruction buffer
                self._kosmos.bas.append(bas_entry)
                # Create an EXECUTE instruction to trigger the MAKE event
                self._kosmos.pes.execute(action=self._kosmos.bas.action_event.SEND)
            # end if
        elif galvanic_emulation:
            # Generate the MAKE user action only for the galvanic part
            bas_entry = self._create_entry(bas_ids=[galvanic_bas_id], state=self.BUTTON_STATE.ON)
            self.send_instructions([bas_entry])
        else:
            # Generate the MAKE user action only for the optical part
            bas_entry = self._create_entry(bas_ids=[optical_bas_id], state=self.BUTTON_STATE.ON)
            self.send_instructions([bas_entry])
        # end if
    # end def hybrid_key_press

    def hybrid_key_release(self, key_id, galvanic_emulation=True, optical_emulation=True, galvanic_optical_delay=0):
        # See ``HybridButtonStimuliInterface.key_release``
        assert key_id in self._button_layout.KEYS, f"The Button emulator don't support the key : {repr(key_id)}"
        assert key_id in self._button_layout.OPTICAL_KEYS, (
            f'The key : {repr(key_id)} is not configured as a hybrid switch')
        assert galvanic_emulation or optical_emulation, ("At least one of the 2 options (i.e. galvanic_emulation or "
                                                         "optical_emulation) must be True")

        bas_ids = list(self._button_layout.KEYS[key_id])
        optical_bas_id = self._button_layout.OPTICAL_KEYS[key_id]
        galvanic_bas_id = bas_ids.copy()
        galvanic_bas_id.remove(optical_bas_id)

        if galvanic_emulation and optical_emulation:
            if galvanic_optical_delay == 0:
                self.key_release(key_id=key_id)
            else:
                first_release = galvanic_bas_id if galvanic_optical_delay > 0 else optical_bas_id
                second_release = optical_bas_id if galvanic_optical_delay > 0 else galvanic_bas_id
                # Generate the RELEASE user action only for the first make (optical or galvanic)
                bas_entry = self._create_entry(bas_ids=[first_release], state=self.BUTTON_STATE.OFF)
                # Add the button entry into the instruction buffer
                self._kosmos.bas.append(bas_entry)
                # Create an EXECUTE instruction to trigger the MAKE event
                self._kosmos.pes.execute(action=self._kosmos.bas.action_event.SEND)
                # Create a DELAY between the make of optical and galvanic part
                self._kosmos.pes.delay(delay_s=abs(galvanic_optical_delay), action=self._kosmos.bas.action_event.SEND)
                # Generate the RELEASE user action only for the second make (optical or galvanic)
                bas_entry = self._create_entry(bas_ids=[second_release], state=self.BUTTON_STATE.OFF)
                # Add the button entry into the instruction buffer
                self._kosmos.bas.append(bas_entry)
                # Create an EXECUTE instruction to trigger the MAKE event
                self._kosmos.pes.execute(action=self._kosmos.bas.action_event.SEND)
            # end if
        elif galvanic_emulation:
            # Generate the RELEASE user action only for the galvanic part
            bas_entry = self._create_entry(bas_ids=[galvanic_bas_id], state=self.BUTTON_STATE.OFF)
            self.send_instructions([bas_entry])
        else:
            # Generate the RELEASE user action only for the optical part
            bas_entry = self._create_entry(bas_ids=[optical_bas_id], state=self.BUTTON_STATE.OFF)
            self.send_instructions([bas_entry])
        # end if
    # end def hybrid_key_release
# end class KosmosHybridButtonEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
