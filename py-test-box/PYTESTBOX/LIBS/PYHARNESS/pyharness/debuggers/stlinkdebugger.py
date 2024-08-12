#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyharness.debuggers.stlinkdebugger
:brief: Debugger operations based on the stlink-tools
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2024/06/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import os
import subprocess
import sys
from abc import ABC
from intelhex import IntelHex

from pyharness.debuggers.nvsdebugger import NvsDebugger
from pylibrary.tools.hexlist import HexList

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
Verbose = False

ST_TRACE = '/usr/local/bin/st-trace'
ST_FLASH = '/usr/local/bin/st-flash'
ST_UTIL = '/usr/local/bin/st-util'
ST_INFO = '/usr/local/bin/st-info'
OUTPUT_FILE = '/tmp/read_flash.bin'

# ----------------------------------------------------------------------------------------------------------------------
# requests
# ----------------------------------------------------------------------------------------------------------------------
ERASE = 'erase'
MAIN_AREA = 'main'
OPTION = 'option'
OPTION_BOOT_AREA = 'option_boot_add'
OPTION_CR = 'optcr'
OPTION_CR_1 = 'optcr1'
OTP_AREA = 'otp'
READ = 'read'
RESET = 'reset'
WRITE = 'write'

# ----------------------------------------------------------------------------------------------------------------------
# Options
# ----------------------------------------------------------------------------------------------------------------------
AREA = '--area'
CHIP_ID = '--chipid'
CONNECT_UNDER_RESET = '--connect-under-reset'
DESCRIPTION = '--descr'
FLASH = '--flash'
FORMAT = '--format'
FREQ = '--freq'
HOT_PLUG = '--hot-plug'
MASS_ERASE = '--mass-erase'
PAGESIZE = '--pagesize'
PROBE = '--probe'
RESET_AFTER = '--reset'
SERIAL = '--serial'
SRAM = '--sram'
VERSION = '--version'


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class STLinkDebugger(NvsDebugger, ABC):
    """
    Implementation of a debugger using the stlink-tools command line programming
    """
    NVS_START_ADDRESS = None
    FLASH_START_ADDRESS = None
    FLASH_SIZE = None
    NVS_SIZE = None
    NVS_BANK_SIZE = None

    def __init__(self, input_dir='.', local_dir=None, debugger_number=0):
        """"
        :param input_dir: input/output directory
        :type input_dir: ``str``
        :param local_dir: The configuration directory.
        :type local_dir: ``str``
        :param debugger_number: Debugger number
        :type debugger_number: ``int``
        """
        super().__init__(input_dir, local_dir, debugger_number)
        self.__next__ = self

        os.environ['LD_LIBRARY_PATH'] = '/usr/local/lib'
        self._stdout = sys.stdout
    # end def __init__

    def _loadConfig(self):
        """
        Load the configuration for the current debugger instance.
        """
        pass
    # end def _loadConfig

    def open(self, **kwargs):
        """
        Open a connection to the debugger, using previously supplied parameters.

        :param kwargs: debugger specific parameters
        :type kwargs: ``any``

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        assert self._openCount == 0, f"Cannot open a {self.__class__.__name__}  instance more than once"

        super().open(**kwargs)
    # end def open

    def reset(self, **kwargs):
        # See ``Debugger.reset``
        process = subprocess.run([ST_FLASH, CONNECT_UNDER_RESET, RESET],
                                 capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"STLink reset operation failed: {process.stderr}"

        return process.returncode
    # end def reset

    def run(self, **kwargs):
        # See ``Debugger.run``
        pass
    # end def run

    def isRunning(self):
        """
        Indicate if the CPU is halted or not

        :return: Flag indicating if the CPU is halted or not.
        :rtype: ``bool``
        """
        raise NotImplementedError
    # end def isRunning

    def stop(self):
        # See ``Debugger.stop``
        pass
    # end def stop

    def __str__(self):
        # See ``Debugger.__str__``
        name = 'STLink Debugger'
        if Verbose:
            self._stdout.write(name + '\n')
        # end if
        return name
    # end def __str__

    # noinspection PyPep8Naming
    def readMemory(self, addressOrLabel, length, memoryType=None):
        # See ``Debugger.readMemory``
        assert isinstance(addressOrLabel, int), TypeError('Should be int instead')

        process = subprocess.run([ST_FLASH, CONNECT_UNDER_RESET, READ, OUTPUT_FILE, hex(addressOrLabel), str(length)],
                                 capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"STLink read operation failed: {process.stdout}"

        with open(OUTPUT_FILE, 'rb') as file:
            buffer = HexList(bytearray(file.read()))
        # end with

        # Delete the file once processed.
        subprocess.run(['rm', OUTPUT_FILE])

        return HexList(buffer)
    # end def readMemory

    # noinspection PyPep8Naming
    def writeMemory(self, addressOrLabel, data, memoryType=None):
        # See ``Debugger.writeMemory``
        pass
    # end def writeMemory

    def erase_firmware(self):
        """
        Erase firmware.

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        process = subprocess.run([ST_FLASH, CONNECT_UNDER_RESET, MASS_ERASE, ERASE,
                                  self.FLASH_START_ADDRESS, self.FLASH_SIZE],
                                 capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"STLink mass erase operation failed: {process.stdout}"
        if process.stdout.count('Mass erase completed successfully.') == 0:
            raise RuntimeError("Unable to erase the target")
        # end if
    # end def erase_firmware

    def flash_firmware(self, firmware_hex_file, no_reset=False):
        """
        Flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``

        :return: Process returned code
        :rtype: ``int``

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        if no_reset:
            process = subprocess.run([ST_FLASH, CONNECT_UNDER_RESET, WRITE, firmware_hex_file],
                                     capture_output=True, universal_newlines=True)
        else:
            process = subprocess.run([ST_FLASH, CONNECT_UNDER_RESET, RESET_AFTER, WRITE, firmware_hex_file],
                                     capture_output=True, universal_newlines=True)
        # end if
        assert process.returncode == 0, f"STLink flashing operation failed: {process.stdout}"
        if process.stdout.count('Flash written and verified! jolly good!') == 0:
            raise RuntimeError("Unable to flash the target")
        # end if

        return process.returncode
    # end def flash_firmware

    def erase_and_flash_firmware(self, firmware_hex_file, no_reset=False):
        """
        Erase and flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``

        :return: Process returned code
        :rtype: ``int``

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        self.erase_firmware()
        return self.flash_firmware(firmware_hex_file, no_reset)
    # end def erase_and_flash_firmware

    def reload_nvs_no_device_reset(self, nvs_hex_file):
        """
        Flashes the NVS part without resetting the device, only stop and run.

        :param nvs_hex_file: Hex file of the NVS to load with the firmware.
                             If None, no NVS is added to the firmware loaded
        :type nvs_hex_file: ``str`` or ``IntelHex``
        """
        # Create a temporary file which is going to be deleted just after the flashing
        flash_hex_file_path = "tmp_merged_files.hex"
        flash_hex_file = IntelHex(nvs_hex_file)

        # Remove all range before NVS address
        # Warning: only the first data block is actually removed !
        flash_hex_file = self.remove_data_block(flash_hex_file, 0, self.NVS_START_ADDRESS)

        flash_hex_file.write_hex_file(flash_hex_file_path)
        status = None
        self.stop()
        self.flash_firmware(firmware_hex_file=flash_hex_file_path)
        self.run()

        return status
    # end def reload_nvs_no_device_reset

    def set_application_bit(self, no_reset=False):
        """
        Select the reboot mode of the firmware.
        Context: NRF52 backward compatibility

        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``
        """
        pass
    # end def set_application_bit

    @staticmethod
    def unlock_target():
        """
        Unlock the device.

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        pass
    # end def unlock_target

    def add_breakpoint(self, address):
        """
        Add a breakpoint to the debugger

        :param address: The address at which to set the breakpoint
        :type address: ``int``

        :return: An integer specifying the trace event handle
        :rtype: ``int``
        """
        raise NotImplementedError
    # end def add_breakpoint

    def clear_breakpoints(self):
        """
        Clear all breakpoints
        """
        raise NotImplementedError
    # end def clear_breakpoints
# end class STLinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class STM32C071Debugger(STLinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the STM32 C071 MCU
    """
    MCU_NAME = 'STM32C071CBU6'
    FLASH_START_ADDRESS = 0x08000000
    FLASH_SIZE = 0x20000
    NVS_START_ADDRESS = 0x08019000
    NVS_SIZE = 0x7000
    NVS_BANK_SIZE = [0x3800, 0x3800]
    CONNECT_UNDER_RESET = True
# end class STM32C071Debugger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
