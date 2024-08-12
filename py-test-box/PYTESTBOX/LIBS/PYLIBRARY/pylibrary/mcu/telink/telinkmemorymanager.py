#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.telink.telinkmemorymanager
:brief: TLSR8-based memory manager classes
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/10/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.mcu.memorymanager import DeviceMemoryManager
from pylibrary.mcu.memorymanager import MemoryManager


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TelinkMemoryManager(MemoryManager):
    """
    TLSR8 memory manager
    """
# end class TelinkMemoryManager


class TLSR8DeviceMemoryManager(TelinkMemoryManager, DeviceMemoryManager):
    """
    TLSR8 based Device Memory Manager Implementation.
    """
# end class TLSR8DeviceMemoryManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
