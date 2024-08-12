#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.memorymanagerfactory
:brief: MCU memory manager factory
:author: Christophe Roquebert <croquebert@logitech.com>
:date:   2020/06/15
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedDeviceMemoryManager
from pylibrary.mcu.nrf52.nrf52memorymanager import Nrf52BasedReceiverMemoryManager
from pylibrary.mcu.nrf54.nrf54memorymanager import Nrf54BasedDeviceMemoryManager
from pylibrary.mcu.stm32.stm32memorymanager import Stm32BasedDeviceMemoryManager
from pylibrary.mcu.telink.telinkmemorymanager import TLSR8DeviceMemoryManager


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MemoryManagerFactory:
    """
    Memory Manager factory creates an object from a given version
    """
    @staticmethod
    def create(debugger, target, config_mgr):
        """
        Create memory manager for MCU

        :param debugger: The debugger object to use to read memory
        :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
        :param target: The target of the memory manager
        :type target: ``str``
        :param config_mgr: Data manager from configuration file depending on context
        :type config_mgr: ``ConfigurationManager``
        """
        if hasattr(debugger, 'MCU_NAME') and debugger.MCU_NAME == 'FakeDebugger':
            return None
        elif hasattr(debugger, 'MCU_NAME') and debugger.MCU_NAME.startswith('NRF52') and 'receiver' in target.lower():
            return Nrf52BasedReceiverMemoryManager(debugger, config_mgr)
        elif hasattr(debugger, 'MCU_NAME') and debugger.MCU_NAME.startswith('NRF52'):
            return Nrf52BasedDeviceMemoryManager(debugger, config_mgr)
        elif hasattr(debugger, 'MCU_NAME') and debugger.MCU_NAME.startswith('NRF54'):
            return Nrf54BasedDeviceMemoryManager(debugger, config_mgr)
        elif hasattr(debugger, 'MCU_NAME') and debugger.MCU_NAME.startswith('STM32'):
            return Stm32BasedDeviceMemoryManager(debugger, config_mgr)
        elif hasattr(debugger, 'MCU_NAME') and debugger.MCU_NAME.startswith('TLSR8'):
            return TLSR8DeviceMemoryManager(debugger, config_mgr)
        else:
            raise NotImplementedError('debugger.MCU_NAME unknown or MCU Memory Manager not implemented')
        # end if
    # end def create
# end class MemoryManagerFactory

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
