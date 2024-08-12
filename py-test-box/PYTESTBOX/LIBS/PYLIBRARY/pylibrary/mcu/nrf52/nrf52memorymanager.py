#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.nrf52memorymanager
:brief: NRF52-based memory manager classes.
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2020/06/15
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from enum import IntEnum

from pylibrary.mcu.memoryinterface import UicrManagerInterface
from pylibrary.mcu.memorymanager import DeviceMemoryManager
from pylibrary.mcu.memorymanager import MemoryManager
from pylibrary.mcu.memorymanager import ReceiverMemoryManager


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Nrf52MemoryManager(MemoryManager, UicrManagerInterface):
    """
    Nrf52 Memory Manager Implementation.
    """
    UICR_REGISTER_RESET_VALUE = 0xFFFFFFFF
    UICR_REGISTER_MAGIC_NUMBER = 0x600DDA7A

    class ADDRESS:
        """
        Address in NRF52 memory map
        """
        class UICROFFSET:
            """
            UICR Data Offset
            """
            NRFFW_0 = 0x014
            BOOTLOADER_ADDRESS = NRFFW_0
            CUSTOMER_0 = 0x080
            NVS_ENCRYPTION_KEY = 0xA0
            MAGIC_NUMBER = 0x0FC
            PSELRESET_0 = 0x200
            PSELRESET_1 = 0x204
            NFCPINS = 0x20C
            DEBUGCTRL = 0x210
            REGOUT0 = 0x304
        # end class UICROFFSET

        N_CUSTOMER_REGISTERS = 32

        UICR_BASE = 0x10001000
        BOOTLOADER_ADDRESS = UICR_BASE + UICROFFSET.BOOTLOADER_ADDRESS
        NVS_ENCRYPTION_KEY = UICR_BASE + UICROFFSET.NVS_ENCRYPTION_KEY
        CUSTOMER_0 = UICR_BASE + UICROFFSET.CUSTOMER_0
        MAGIC_NUMBER = UICR_BASE + UICROFFSET.MAGIC_NUMBER
        PSELRESET_0 = UICR_BASE + UICROFFSET.PSELRESET_0
        PSELRESET_1 = UICR_BASE + UICROFFSET.PSELRESET_1
        NFCPINS = UICR_BASE + UICROFFSET.NFCPINS
        DEBUGCTRL = UICR_BASE + UICROFFSET.DEBUGCTRL
        REGOUT0 = UICR_BASE + UICROFFSET.REGOUT0
    # end class ADDRESS

    class SIZE(IntEnum):
        """
        Data Size
        """
        UICR_REGISTER = 0x04
        BOOTLOADER_ADDRESS = 0x04
        NVS_ENCRYPTION_KEY = 0x10
    # end class SIZE
# end class Nrf52MemoryManager


class Nrf52BasedDeviceMemoryManager(Nrf52MemoryManager, DeviceMemoryManager):
    """
    Nrf52-based Device Memory Manager Implementation.
    """
# end class Nrf52BasedDeviceMemoryManager


class Nrf52BasedReceiverMemoryManager(Nrf52MemoryManager, ReceiverMemoryManager):
    """
    Nrf52-based Receiver Memory Manager Implementation.
    """
# end class Nrf52BasedReceiverMemoryManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
