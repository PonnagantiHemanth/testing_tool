#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pylibrary.mcu.stm32.stm32memorymanager
:brief: STM32-based memory manager classes
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2023/08/29
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from copy import deepcopy

from pylibrary.mcu.memorymanager import DeviceMemoryManager
from pylibrary.mcu.memorymanager import MemoryManager
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Stm32MemoryManager(MemoryManager):
    """
    STM32 memory manager
    """
    def load_nvs(self, backup=False, no_reset=False, **kwargs):
        # See ``MemoryManage.load_nvs``
        self.debugger._j_link.reset(halt=True)
        # Erase before loading
        self.debugger.writeMemory(self.debugger.NVS_START_ADDRESS, HexList("FF" * self.debugger.NVS_SIZE))
        super().load_nvs(backup, no_reset, **kwargs)
    # end def load_nvs
# end class Stm32MemoryManager


class Stm32BasedDeviceMemoryManager(Stm32MemoryManager, DeviceMemoryManager):
    """
    STM32 based Device Memory Manager Implementation.
    """

    SECURE_LVL_APP_INDEX = 0
    SECURE_LVL_IMG_INDEX = 1

    def __init__(self, debugger, config_mgr):
        # See ``MemoryManager.__init__``
        super().__init__(debugger, config_mgr)
        self.secure_nvs = None
        self._backup_secure_nvs = None
    # end def __init__

    def exclude_flash_cache_all_nvs(self):
        """
        Exclude all NVS from the internal cache of the jlink probe.
        Note: As the jlink library allows to exclude only one range, this method may exclude more than necessary,
        if NVS and NVS secure are not following
        """
        start_address = min(self.debugger.NVS_START_ADDRESS, self.debugger.SECURE_BLOCK_START_ADDRESS)
        stop_address = max(self.debugger.NVS_START_ADDRESS + self.debugger.NVS_SIZE,
                           self.debugger.SECURE_BLOCK_START_ADDRESS + self.debugger.NVS_SECURE_SIZE)
        self.debugger.exclude_flash_cache_range(start_address=start_address, stop_address=stop_address)
    # end def exclude_flash_cache_all_nvs

    def read_secure_nvs(self):
        """
        Read secure NVS
        """
        self.exclude_flash_cache_all_nvs()
        self.secure_nvs = self.debugger.readMemory(self.debugger.SECURE_BLOCK_START_ADDRESS,
                                                   self.debugger.NVS_SECURE_SIZE)
    # end def read_secure_nvs

    def backup_secure_nvs(self):
        """
        Backup secure NVS
        """
        if self.secure_nvs is None:
            self.read_secure_nvs()
        # end if
        self._backup_secure_nvs = deepcopy(self.secure_nvs)
    # end def backup_secure_nvs

    def write_secure_nvs(self, secure_nvs_data):
        """
        Write secure NVS

        :param secure_nvs_data: Secure NVS data
        :type secure_nvs_data: ``HexList``
        """
        self.debugger.writeMemory(self.debugger.SECURE_BLOCK_START_ADDRESS, secure_nvs_data)
    # end def write_secure_nvs

    def restore_secure_nvs(self):
        """
        Restore secure NVS
        """
        assert self._backup_secure_nvs is not None
        self.write_secure_nvs(secure_nvs_data=self._backup_secure_nvs)
    # end def restore_secure_nvs

    def get_security_level_chunk(self):
        """
        Get security level chunk

        :return: Security level chunk and security level index
        :rtype: ``tuple[HexList, int]``
        """
        if self.secure_nvs is None:
            self.read_secure_nvs()
        # end if
        secur_lvl_chunk = None
        secur_lvl_chunk_start = None
        for secur_lvl_chunk_start in range(0, len(self.secure_nvs), self.chunk_id_map["NVS_WORD_SIZE"]):
            secur_lvl_chunk = self.secure_nvs[
                              secur_lvl_chunk_start:secur_lvl_chunk_start + self.chunk_id_map["NVS_WORD_SIZE"]]
            if (self.secure_nvs[secur_lvl_chunk_start + self.chunk_id_map["NVS_WORD_SIZE"]:
                                secur_lvl_chunk_start + 2 * self.chunk_id_map["NVS_WORD_SIZE"]] ==
                    HexList("FF" * self.chunk_id_map["NVS_WORD_SIZE"])):
                break
            # end if
        # end for
        return secur_lvl_chunk, secur_lvl_chunk_start // self.chunk_id_map["NVS_WORD_SIZE"]
    # end def get_security_level_chunk

    def get_security_level_application(self):
        """
        Get security level of application

        :return: Security level of application
        :rtype: ``HexList``
        """
        secur_lvl_chunk, _ = self.get_security_level_chunk()
        return secur_lvl_chunk[self.SECURE_LVL_APP_INDEX]
    # end def get_security_level_application

    def set_security_level(self, security_level, index):
        """
        Set security level at given index

        :param security_level: Security level
        :type security_level: ``int``
        :param index: Index of the security level in the chunk
        :type index: ``int``
        """
        secur_lvl_chunk, secur_lvl_chunk_index = self.get_security_level_chunk()
        if secur_lvl_chunk[index] != security_level:
            secur_lvl_chunk[index] = security_level
            next_chunk_start = (secur_lvl_chunk_index + 1) * self.chunk_id_map["NVS_WORD_SIZE"]
            self.secure_nvs[next_chunk_start : next_chunk_start + self.chunk_id_map["NVS_WORD_SIZE"]] = secur_lvl_chunk
            self.debugger.writeMemory(self.debugger.SECURE_BLOCK_START_ADDRESS + next_chunk_start, secur_lvl_chunk)
        # end if
    # end def set_security_level_chunk

    def set_security_level_application(self, security_level):
        """
        Set security level of application

        :param security_level: Security level
        :type security_level: ``int``
        """
        self.set_security_level(security_level=security_level, index=self.SECURE_LVL_APP_INDEX)
    # end def set_security_level_application
# end class Stm32BasedDeviceMemoryManager

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
