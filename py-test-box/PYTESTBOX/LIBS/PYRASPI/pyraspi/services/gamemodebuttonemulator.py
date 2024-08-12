#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyraspi.services.gamemodebuttonemulator
:brief: Game Mode Control Class
:author: Zane Lu <zlu@logitech.com>
:date: 2023/07/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------

from pylibrary.emulator.emulatorinterfaces import GameModeEmulationInterface
from pylibrary.emulator.keyid import KEY_ID


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GameModeButtonEmulator(GameModeEmulationInterface):
    """
    Game Mode Button emulator
    """
    def __init__(self, button_emulator):
        """
        :param button_emulator: the instance of ButtonStimuliInterface
        :type button_emulator: ``ButtonStimuliInterface``
        """
        self.button_emulator = button_emulator
        self.state = GameModeEmulationInterface.MODE.DISABLED
    # end def __init__

    def get_state(self):
        # See ``GameModeEmulationInterface.get_state``
        return self.state
    # end def get_state

    def set_mode(self, activate_game_mode=False):
        # See ``GameModeEmulationInterface.set_mode``
        if not activate_game_mode:
            if self.state == GameModeEmulationInterface.MODE.ENABLED:
                self.button_emulator.keystroke(key_id=KEY_ID.GAME_MODE_KEY)
                self.state = GameModeEmulationInterface.MODE.DISABLED
            # end if
        else:
            if self.state == GameModeEmulationInterface.MODE.DISABLED:
                self.button_emulator.keystroke(key_id=KEY_ID.GAME_MODE_KEY)
                self.state = GameModeEmulationInterface.MODE.ENABLED
            # end if
        # end if
    # end def set_mode
# end class GameModeButtonEmulator

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
