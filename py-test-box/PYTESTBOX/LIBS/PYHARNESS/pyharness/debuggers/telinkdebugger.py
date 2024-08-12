#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyharness.debuggers.telinkdebugger
:brief: Debugger operations based on the Telink LinuxBDT API
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/10/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import re
import subprocess
import sys
from abc import ABC

from intelhex import IntelHex

from pyharness.debuggers.nvsdebugger import NvsDebugger
from pylibrary.tools.hexlist import HexList

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
Verbose = False

LINUX_BDT = '/opt/Telink/LinuxBDT/bdt'
MODEL = 'b80'
# -----------------
# LinuxBDT requests
# -----------------
VERSION = '-v'
ACTIVATE = 'ac'
CONNECT = 'sws'
UNLOCK = 'ulf'
FLASH = 'wf '
WRITE = 'wc'
READ = 'rc'
RUN = 'run'
STOP = 'pause'
RESET = 'rst'
# -------
# Options
# -------
FORCE = '-f'
SIZE = '-s'
ERASE = '-e'
INPUT = '-i'
# ----------
# Parameters
# ----------
START_ADDRESS = 0
FLASH_SIZE = '1016k'
# -----------
# Constraints
# -----------
WRITE_BLOCK_SIZE = 94


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TelinkDebugger(NvsDebugger, ABC):
    """
    Implementation of a debugger using TLSR8208C command line programming under Linux (i.e. LinuxBDT).
    """
    VERSION = None

    NVS_START_ADDRESS = None
    NVS_SIZE = None
    NVS_BANK_SIZE = None

    def __init__(self, input_dir='.', local_dir=None, debugger_number=0):
        """
        :param input_dir: input/output directory
        :type input_dir: ``str``
        :param local_dir: The configuration directory.
        :type local_dir: ``str``
        :param debugger_number: Debugger number
        :type debugger_number: ``int``
        """
        super().__init__(input_dir, local_dir, debugger_number)
        self.__next__ = self

        # Get Telink library version
        self.VERSION = self.getVersion()
        major, minor, patch = tuple(map(int, self.VERSION.split('.')))
        assert (major == 1)
        assert (minor == 5)
        assert (patch >= 3)

        self._stdout = sys.stdout
    # end def __init__

    def getVersion(self):
        # See ``Debugger.getVersion``
        process = subprocess.run([LINUX_BDT, MODEL, VERSION], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT get version subprocess failed: {process.stdout}"
        return process.stdout.split('bdt version: ')[1].strip()
    # end def getVersion

    @staticmethod
    def wake_up():
        """
        Run this command when the firmware is in low power mode

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        process = subprocess.run([LINUX_BDT, MODEL, ACTIVATE], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT activate subprocess failed: {process.stdout}"
        if process.stdout.count('Activate OK!') == 0:
            raise RuntimeError("Unable to activate the LinuxBDT link")
        # end if
    # end def wake_up

    # --------------------------------------------------------------------------
    def _loadConfig(self):
        """
        Load the configuration for the current debugger instance.
        """
        pass

    # end def _loadConfig

    def open(self, unlock_device=False, **kwargs):
        """
        Open a connection to the debugger, using previously supplied parameters.

        :param unlock_device: Unlock the device if needed before the call to connect - OPTIONAL
        :type unlock_device: ``bool``
        :param kwargs: debugger specific parameters
        :type kwargs: ``any``

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        assert self._openCount == 0, f"Cannot open a {self.__class__.__name__}  instance more than once"

        super().open(**kwargs)

        if unlock_device:
            self.unlock_target()
        # end if

        # Get the target out of the low power mode
        self.wake_up()

        process = subprocess.run([LINUX_BDT, MODEL, CONNECT], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT connect subprocess failed: {process.stdout}"
        if process.stdout.count('TC32 EVK: Swire ok!') == 0:
            raise RuntimeError("Unable to connect to the probe")
        # end if
    # end def open

    def reset(self, **kwargs):
        # See ``Debugger.reset``
        process = subprocess.run([LINUX_BDT, MODEL, RESET, FORCE], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT reset subprocess failed: {process.stdout}"
        if process.stdout.count('reset mcu') == 0:
            raise RuntimeError("Unable to reset the target")
        # end if

        return process.returncode
    # end def reset

    def run(self, **kwargs):
        """
        Restart the CPU core if it was previously halted.

        :param kwargs: debugger specific parameters
        :type kwargs: ``any``

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        process = subprocess.run([LINUX_BDT, MODEL, RUN], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT run subprocess failed: {process.stdout}"
        if process.stdout.count('mcu run') == 0:
            raise RuntimeError("Unable to run the target")
        # end if

        if Verbose:
            self._stdout.write('Run the target\n')
        # end if
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
        process = subprocess.run([LINUX_BDT, MODEL, STOP], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT stop subprocess failed: {process.stdout}"
        if process.stdout.count('pause mcu') == 0:
            raise RuntimeError("Unable to stop the target")
        # end if

        if Verbose:
            self._stdout.write('Stop the debugger\n')
        # end if
        return 0
    # end def stop

    def __str__(self):
        # See ``Debugger.__str__``
        name = 'Telink Debugger'
        if Verbose:
            self._stdout.write(name + '\n')
        # end if
        return name
    # end def __str__

    # noinspection PyPep8Naming
    def readMemory(self, addressOrLabel, length, memoryType=None):
        # See ``Debugger.readMemory``
        assert isinstance(addressOrLabel, int), TypeError('Should be int instead')

        process = subprocess.run([LINUX_BDT, MODEL, READ, hex(addressOrLabel), SIZE, str(length)],
                                 capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT read subprocess failed: {process.stdout}"
        address_str = str(addressOrLabel) if addressOrLabel != 0 else '0'
        if process.stdout.count(address_str + ':') == 0:
            raise RuntimeError(f"Unable to read address {address_str}")
        # end if

        buffer = []
        data_extractor = re.compile(r'[\s*][0x]{0,2}([0-9]{1,8}):  ([0-9a-f\s]*)')
        for line in process.stdout.split('\n'):
            hub_id_matching = data_extractor.search(line)
            if hub_id_matching:
                # save entry in hub identifier list
                buffer.append(hub_id_matching.group(2).replace(' ', ''))
            # end if
        # end for
        return HexList(buffer)
    # end def readMemory

    # noinspection PyPep8Naming
    def writeMemory(self, addressOrLabel, data, memoryType=None):
        # See ``Debugger.writeMemory``
        address = self.getAddress(addressOrLabel, memoryType)

        for block_count in range((len(data) + WRITE_BLOCK_SIZE - 1) // WRITE_BLOCK_SIZE):
            start = block_count*WRITE_BLOCK_SIZE
            # Compute the write data size knowing that it could not be greater than WRITE_BLOCK_SIZE
            size = WRITE_BLOCK_SIZE if len(data[start:]) > WRITE_BLOCK_SIZE else len(data[start:])
            formatted_data = [str(data)[i:i + 2] for i in range(start, start + size)]
            process = subprocess.run([LINUX_BDT, MODEL, WRITE, str(address + start)] + formatted_data +
                                     [SIZE, str(size)], capture_output=True, universal_newlines=True)
            assert process.returncode == 0, f"LinuxBDT write subprocess failed: {process.stdout}"
            if process.stdout.count(f'Write {size} bytes at address') == 0:
                raise RuntimeError(f"Unable to write {size} bytes of the data at address {address + start}")
            # end if
        # end for
    # end def writeMemory

    @staticmethod
    def erase_firmware():
        """
        Erase firmware.

        :raise ``AssertionError``: if running subprocess fails
        :raise ``RuntimeError``: if the expected returned message is not found in stdout
        """
        process = subprocess.run([LINUX_BDT, MODEL, FLASH, START_ADDRESS, SIZE, FLASH_SIZE, ERASE],
                                 capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT erase subprocess failed: {process.stdout}"
        if process.stdout.count('EraseSectorsize...') == 0:
            raise RuntimeError("Unable to erase the target")
        # end if
    # end def erase_firmware

    @staticmethod
    def flash_firmware(firmware_hex_file, no_reset=False):
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
        process = subprocess.run([LINUX_BDT, MODEL, FLASH, START_ADDRESS, INPUT, firmware_hex_file],
                                 capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT flashing subprocess failed: {process.stdout}"
        if process.stdout.count('File Download to Flash at address 0x000000:') == 0:
            raise RuntimeError("Unable to flash the target")
        # end if

        if not no_reset:
            process = subprocess.run([LINUX_BDT, MODEL, RESET],
                                     capture_output=True, universal_newlines=True)
            assert process.returncode == 0, f"LinuxBDT reset subprocess failed: {process.stdout}"
            if process.stdout.count('reset mcu') == 0:
                raise RuntimeError("Unable to reset the target")
            # end if
        # end if

        return process.returncode
    # end def flash_firmware

    def erase_and_flash_firmware(self, firmware_hex_file, no_reset=False):
        """
        Erase and flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str`` or ``IntelHex``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``
        """
        self.erase_firmware()
        if self.NVS_START_ADDRESS is not None and self.NVS_SIZE is not None:
            nvs = self.readMemory(addressOrLabel=self.NVS_START_ADDRESS, length=self.NVS_SIZE)
            assert nvs == HexList("FF" * self.NVS_SIZE), "NVS should be erased"
        # end if
        self.flash_firmware(firmware_hex_file, no_reset)
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
        process = subprocess.run([LINUX_BDT, MODEL, UNLOCK], capture_output=True, universal_newlines=True)
        assert process.returncode == 0, f"LinuxBDT subprocess failed: {process.stdout}"
        if process.stdout.count('unlock') == 0:
            raise RuntimeError("Unable to unlock the device")
        # end if
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
# end class TelinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class TLSR8208CDebugger(TelinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Meson MCU.
    """
    MCU_NAME = 'TLSR8208C'
    NVS_START_ADDRESS = 0x3C000
    NVS_SIZE = 16 * 1024
    NVS_BANK_SIZE = 8 * 1024
# end class TLSR8208CDebugger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
