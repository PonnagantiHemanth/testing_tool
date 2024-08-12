#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyharness.debuggers.nvsdebugger
:brief: Debugger NVS management mixin class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/10/30
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import subprocess
import sys
from abc import ABC
from contextlib import contextmanager
from os import listdir
from os.path import exists
from os.path import isfile
from os.path import join
from typing import TextIO

from intelhex import IntelHex

from pylibrary.system.debugger import Debugger
from pylibrary.tools.config import ConfigParser
from pylibrary.tools.elfhelper import ElfHelper
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# SEGGER Identifier
SEGGER_VENDOR_ID = 0x1366
ST_MICROELECTRONICS_VENDOR_ID = 0x0483

RTT_BUFFER_SYMBOL = '_SEGGER_RTT'


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NvsDebugger(Debugger, ABC):
    """
    Define debugger mixin class adding NVS management capability
    """
    CONNECT_UNDER_RESET = False
    MCU_NAME = None
    NVS_START_ADDRESS = None
    NVS_SIZE = None
    NVS_BANK_SIZE = None

    _serial_no: int = 0
    _stdout: TextIO = None

    @contextmanager
    def opened_with_mcu_name(self, mcu_name, unlock_device=False, exclude_nvs_range=True, **kwargs):
        """
        Enable the use of a debugger configured for a different MCU than the default one stored in ``MCU_NAME``.
        It will change its ``MCU_NAME`` value to the wanted one, perform the wanted task and change its ``MCU_NAME``
        value back to the original one.

        This method has to close the debugger (if needed) and open it for the change in MCU name to take effect.
        This method follows the rule that a state not related to the function of the method should be the same at the
        entry and the exit of said method, therefore the open/closed state of the debugger will be the same at the
        exit of this method (even if the method opens it for what is inside the with).

        :param mcu_name: The wanted MCU name
        :type mcu_name: ``str``
        :param unlock_device: ``unlock_device`` parameter for the open method for inside the with - OPTIONAL
        :type unlock_device: ``bool``
        :param exclude_nvs_range: Flag indicating to exclude NVS addresses in the cached range - OPTIONAL
        :type exclude_nvs_range: ``bool``
        :param kwargs: ``kwargs`` parameter for the open method for inside the with - OPTIONAL
        :type kwargs: ``any``
        """
        backup_debugger_mcu_name = self.MCU_NAME

        open_at_the_beginning = self.isOpen()

        try:
            if backup_debugger_mcu_name != mcu_name:
                if open_at_the_beginning:
                    self.close()
                # end if
                self.MCU_NAME = mcu_name
                self.open(unlock_device=unlock_device, exclude_nvs_range=exclude_nvs_range, **kwargs)
            elif not open_at_the_beginning:
                self.open(unlock_device=unlock_device, exclude_nvs_range=exclude_nvs_range, **kwargs)
            # end if
            yield
        finally:
            if backup_debugger_mcu_name != mcu_name:
                self.close()
                self.MCU_NAME = backup_debugger_mcu_name
                if open_at_the_beginning:
                    self.open()
                # end if
            elif not open_at_the_beginning:
                self.close()
            # end if
        # end try
    # end def opened_with_mcu_name

    @contextmanager
    def closed(self):
        """
        Close debugger while executing.
        """
        open_at_the_beginning = self.isOpen()
        if open_at_the_beginning:
            self.close()
        # end if
        try:
            yield
        finally:
            if open_at_the_beginning:
                self.open()
            # end if
        # end try
    # end def closed

    def set_stdout(self, stdout):
        """
        Set stdout attribute

        :param  stdout: Stream for output
        :type stdout: ``stream``
        """
        self._stdout = stdout
    # end def set_stdout

    def get_device(self):
        """
        Get device name attribute

        :return: MCU name
        :rtype: ``str``
        """
        return self.MCU_NAME
    # end def get_device

    # --------------------------------------------------------------------------
    _SECTION_CONNECTION = 'CONNECTION'
    _KEY_SERIAL_NO = 'serial_no_'
    _KEY_RTT_BUFFER_ADDRESS = 'rtt_buffer_address'

    def _loadConfig(self):
        """
        Load the configuration for the current debugger instance.
        """
        file_path = join(self._localDir, 'debugger.ini')

        config = ConfigParser()

        if isfile(file_path):
            config.read([file_path])
        else:
            config.add_section(self._SECTION_CONNECTION)

            number_list = []
            if sys.platform == 'linux':
                # Try to guess a possible J-Link match using SEGGER Vendor ID
                segger_vid = '%x' % SEGGER_VENDOR_ID
                # lsusb -v -d 1366: | grep -oP 'iSerial +[0-9] \K[0-9]+':
                #    can't get device qualifier: Resource temporarily unavailable
                #    can't get debug descriptor: Resource temporarily unavailable
                # 2>/dev/null is added to avoid errors that do not concern us. However, it could mask some others.
                # This is a quick fix that will need to be handled more properly in the future
                # We know that the issue came with a more recent release of RaspberryPi OS.
                completed_process = subprocess.run(
                    f'lsusb -v -d {segger_vid}: 2>/dev/null | grep -oP "iSerial +[0-9] \\K[0-9]+"',
                    shell=True,
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, universal_newlines=True)
                assert (completed_process.returncode == 0)
                number_list = completed_process.stdout.rstrip().split('\n')
            else:
                number_list.append(self._serial_no)
            # end if

            if len(number_list) == 1:
                config.set(self._SECTION_CONNECTION,
                           '%s%d' % (self._KEY_SERIAL_NO, self.number),
                           int(number_list[0]))
            else:
                number_list.sort(reverse=True)
                for index in range(len(number_list)):
                    config.set(self._SECTION_CONNECTION,
                               '%s%d' % (self._KEY_SERIAL_NO, index),
                               int(number_list[index]))
                # end for
            # end if

            # RTT Buffer address retrieval
            rtt_buffer_address = None
            elf_file_path = join(TESTS_PATH, "DFU_FILES")
            if exists(elf_file_path):
                for file in listdir(elf_file_path):
                    if file.endswith(".elf"):
                        # Look for the symbol in the elf
                        app_elf_helper = ElfHelper(join(elf_file_path, file))
                        rtt_buffer_address = app_elf_helper.get_symbol_address(RTT_BUFFER_SYMBOL)
                        if rtt_buffer_address is not None:
                            break
                        # end if
                    # end if
                # end for
            # end if

            config.set(self._SECTION_CONNECTION, str(self._KEY_RTT_BUFFER_ADDRESS), rtt_buffer_address)

            with open(file_path, 'w+') as fp:
                config.write(fp)
            # end with
        # end if

        self._serial_no = config.get(self._SECTION_CONNECTION, '%s%d' % (self._KEY_SERIAL_NO, self.number))
        self._rtt_buffer_address = config.get(self._SECTION_CONNECTION, str(self._KEY_RTT_BUFFER_ADDRESS))
    # end def _loadConfig

    @staticmethod
    def flash_firmware(firmware_hex_file, no_reset=False):
        """
        Flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str``
        :param no_reset: If True, the device stays halted after the flashing. Otherwise, it runs - OPTIONAL
        :type no_reset: ``bool``

        :return: Status
        :rtype: ``int``
        """
        raise NotImplementedError
    # end def flash_firmware

    def remove_uicr_block(self, flash_hex_file):
        """
        Delete the UICR data block from the given binary file (Implemented in NRF52 class only)

        :param flash_hex_file: Firmware Hex file
        :type flash_hex_file: ``IntelHex``

        :return: Modified firmware Hex file
        :rtype: ``IntelHex``
        """
        raise NotImplementedError
    # end def remove_uicr_block

    def reload_file(self, firmware_hex_file=None, nvs_hex_file=None, no_reset=False):
        """
        Flash the device. At least one of the two OPTIONAL hex file parameters should be not None.

        :param firmware_hex_file: Hex file of the firmware to load - OPTIONAL
        :type firmware_hex_file: ``str`` or ``IntelHex``
        :param nvs_hex_file: Hex file of the NVS to load with the firmware.
                             If None, no NVS is added to the firmware loaded - OPTIONAL
        :type nvs_hex_file: ``str`` or ``IntelHex``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``

        :return: Status
        :rtype: ``int``
        """
        assert not (firmware_hex_file is None and nvs_hex_file is None), "At least one file is required"

        flash_hex_file = IntelHex(firmware_hex_file)

        if nvs_hex_file is not None:
            nvs_intel_hex = IntelHex(nvs_hex_file)
            if nvs_intel_hex.minaddr() != self.NVS_START_ADDRESS or len(nvs_intel_hex.addresses()) != self.NVS_SIZE:
                nvs_bin_array_pad = nvs_intel_hex.tobinarray(start=self.NVS_START_ADDRESS, size=self.NVS_SIZE)
                nvs_intel_hex_pad = IntelHex()
                nvs_intel_hex_pad.frombytes(nvs_bin_array_pad, offset=self.NVS_START_ADDRESS)
            else:
                nvs_intel_hex_pad = nvs_intel_hex
            # end if
            flash_hex_file.merge(nvs_intel_hex_pad, 'replace')
        else:
            start_address = self.NVS_START_ADDRESS
            bank_size_list = self.NVS_BANK_SIZE if isinstance(self.NVS_BANK_SIZE, list) else [self.NVS_BANK_SIZE]
            for bank_size in bank_size_list:
                # Erase first bank
                flash_hex_file = self.remove_data_block(flash_hex_file, start_address, bank_size)
                start_address += bank_size
                # Erase second bank
                flash_hex_file = self.remove_data_block(flash_hex_file, start_address, bank_size)
                start_address += bank_size
            # end for
        # end if

        if self.MCU_NAME.startswith('NRF52'):
            flash_hex_file = self.remove_uicr_block(flash_hex_file)
        # end if

        return self.flash_firmware(flash_hex_file, no_reset)
    # end def reload_file

    @staticmethod
    def remove_data_block(file, start_address, size):
        """
        Delete all data blocks included into the specified address range.
        """
        for address in range(start_address, start_address+size, 1):
            # noinspection PyBroadException
            try:
                del file[address]
            except Exception:
                # Do not warn if address does not exist but jump to the next one
                continue
            # end try
        # end for
        return file
    # end def remove_data_block
# end class NvsDebugger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
