#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.nrf54memorymanager
:brief: NRF54-based memory manager classes.
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/03/12
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.mcu.memorymanager import DeviceMemoryManager
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52MemoryManager


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Nrf54BasedDeviceMemoryManager(Nrf52MemoryManager, DeviceMemoryManager):
    """
    Nrf54-based Device Memory Manager Implementation.
    """

    class ADDRESS(Nrf52MemoryManager.ADDRESS):
        """
        Address in memory map
        """
        NVS_ENCRYPTION_KEY = None
    # end class ADDRESS
# end class Nrf54BasedDeviceMemoryManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
