#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyharness.debuggers.nrfprobedebugger
:brief: Debugger using NRF Probe lib
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/01/22
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from abc import ABC
from os import remove
from time import sleep

from intelhex import IntelHex
from nrf_probe_py import CoreId
from nrf_probe_py import Erase
from nrf_probe_py import Probe
from nrf_probe_py import ProbeError
from nrf_probe_py import Reset
from nrf_probe_py import Verify
from nrf_probe_py import enable_logging
from nrf_probe_py import version

from pyharness.debuggers.nvsdebugger import NvsDebugger
from pylibrary.system.debugger import Debugger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.tracebacklog import TracebackLogWrapper

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
VERBOSE = False

# NRF54 restart timing
REBOOT_TIME = .3


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class NrfProbeDebugger(NvsDebugger, ABC):
    """
    Implementation of a debugger using nrf_probe_lib package (support NRF54xx chips only).
    """
    VERSION = '0.3.1'

    NVS_START_ADDRESS = None
    NVS_SIZE = None
    NVS_BANK_SIZE = None

    UICR_START_ADDRESS = None

    def __init__(self, input_dir='.', local_dir=None, debugger_number=0):
        """
        :param input_dir: input/output directory - OPTIONAL
        :type input_dir: ``str``
        :param local_dir: The configuration directory - OPTIONAL
        :type local_dir: ``str``
        :param debugger_number: Debugger number - OPTIONAL
        :type debugger_number: ``int``
        """
        super().__init__(input_dir, local_dir, debugger_number)
        self.__next__ = self

        self._stdout = sys.stdout
        self._serial_no = 0
        self._rtt_buffer_address = None
        self._probe = None
    # end def __init__

    def open(self, unlock_device=False, exclude_nvs_range=True, **kwargs):
        """
        Open a connection to the debugger, using previously supplied parameters.

        :param unlock_device: Unlock the device before the call to connect (unused for nRF54 devices) - OPTIONAL
        :type unlock_device: ``bool``
        :param exclude_nvs_range: Flag indicating to exclude NVS addresses in the cached range (unused) - OPTIONAL
        :type exclude_nvs_range: ``bool``
        :param kwargs: debugger specific parameters
        :type kwargs: ``any``
        """
        assert self._openCount == 0, f"Cannot open a {self.__class__.__name__}  instance more than once"

        super().open(**kwargs)

        self._probe = Probe(serial_number=int(self._serial_no), timeout_ms=2000)

        if VERBOSE:
            enable_logging()
        # end if
        self._openCount += 1
    # end def open

    def close(self):
        """
        Close a connection to the debugger.
        """
        if self._openCount == 0:
            return
        # end if

        super().close()

        if self._openCount == 1 and self._probe is not None:
            self._probe.close()
            del self._probe
            self._probe = None
        # end if

        if self._openCount > 0:
            self._openCount -= 1
        # end if
    # end def close

    def reset(self, soft_reset=True, skip_current_breakpoint=True):
        """
        Reset the nrf probe lib debugger.

        :param soft_reset: flag to select between a soft reset and an emulated power on reset - OPTIONAL
        :type soft_reset: ``bool``
        :param skip_current_breakpoint: flag to stop on / skip (default) the current breakpoint - OPTIONAL
        :type skip_current_breakpoint: ``bool``
        """
        if self._probe is not None:
            if soft_reset:
                # Soft reset
                self._probe.reset(reset_kind=Reset.SOFT)
            else:
                # Emulate a power-on-reset
                self._probe.reset(reset_kind=Reset.HARD)
                # Time to let the DUT reboot
                sleep(REBOOT_TIME)
            # end if
        # end if
        return 0
    # end def reset

    def run(self, skip_current_breakpoint=True):
        """
        Restarts the CPU core if it was previously halted.

        :param skip_current_breakpoint: flag to stop on / skip (default) the current breakpoint (unused) - OPTIONAL
        :type skip_current_breakpoint: ``bool``
        """
        if self._probe is not None and self._probe.is_halted():
            self._probe.go()
        # end if

        if VERBOSE:
            self._stdout.write('RUN of the simulator')
        # end if
    # end def run

    def isRunning(self):
        """
        Indicate if the CPU is halted or not

        :return: Flag indicating if the CPU is halted or not.
        :rtype: ``bool``
        """
        if self._probe is not None and not self._probe.is_halted():
            if VERBOSE:
                self._stdout.write('simulator is RUNNING')
            # end if
            return True
        else:
            if VERBOSE:
                self._stdout.write('simulator is NOT RUNNING')
            # end if
            return False
        # end if
    # end def isRunning

    def stop(self):
        """
        Stop the CPU core if it was not previously halted.

        :return: Hard coded status at 0
        :rtype: ``int``
        """
        if self._probe is not None and not self._probe.is_halted():
            self._probe.halt(core=CoreId.APPLICATION)
        # end if

        if VERBOSE:
            self._stdout.write('STOP of the simulator')
        # end if
        return 0
    # end def stop

    # noinspection PyPep8Naming
    # noinspection PyShadowingBuiltins
    def loadCoverage(self, filePath, format=Debugger.FORMAT_COMMON):
        """
        @copydoc pylibrary.system.debugger.Debugger.loadCoverage
        """
        raise NotImplementedError
    # end def loadCoverage

    # noinspection PyPep8Naming
    # noinspection PyShadowingBuiltins
    def saveCoverage(self, filePath, format=Debugger.FORMAT_COMMON):
        """
        @copydoc pylibrary.system.debugger.Debugger.saveCoverage
        """
        raise NotImplementedError
    # end def saveCoverage

    def __str__(self):
        """
        Retrieve debugger's name

        :return: debugger name
        :rtype: ``str``
        """
        name = 'NRF Probe lib Debugger'
        if VERBOSE and self._probe is not None:
            self._stdout.write(self._probe.get_firmware_version())
        # end if
        return name
    # end def __str__

    def getVersion(self):
        """
        Obtain the version of this debugger.

        :return: The debugger version
        :rtype: ``str``
        """
        return version()
    # end def getVersion

    # noinspection PyPep8Naming
    def getRegisters(self, registersList):
        """
        @copydoc pylibrary.system.debugger.Debugger.getRegisters
        """
        raise NotImplementedError
    # end def getRegisters

    def get_registers_definition(self):
        """
        Get the definition of the registers

        @return (dict) Definition of the registers
        """
        raise NotImplementedError
    # end def get_registers_definition

    _registers = property(get_registers_definition)

    # noinspection PyPep8Naming
    def readMemory(self, addressOrLabel, length, memoryType=CoreId.APPLICATION):
        """
        @copydoc pylibrary.system.debugger.Debugger.readMemory
        """
        assert isinstance(addressOrLabel, int), TypeError('Should be int instead')
        assert memoryType in [CoreId.APPLICATION, CoreId.NETWORK]

        try:
            buffer = self._probe.memread(addr=addressOrLabel, len=length, core=memoryType)
            return HexList(buffer)
        except (ProbeError, ValueError):
            self._stdout.write(f"NRF Probe lib Debugger readMemory failed, retry with halting the device: "
                               f"{TracebackLogWrapper.get_exception_stack()}\n")
        # end try
    # end def readMemory

    # noinspection PyPep8Naming
    def writeMemory(self, addressOrLabel, data, memoryType=CoreId.APPLICATION):
        """
        @copydoc corepython.system.debugger.Debugger.writeMemory
        """
        assert memoryType in [CoreId.APPLICATION, CoreId.NETWORK]

        address = self.getAddress(addressOrLabel, memoryType)
        if self._probe is not None:
            return self._probe.memwrite(addr=address, data=list(data), core=memoryType)
        else:
            raise RuntimeError("Unable to write memory")
        # end if
    # end def writeMemory

    def erase_firmware(self, memory_type=CoreId.APPLICATION):
        """
        Erase the firmware of a Core identified by its unique id.

        :param memory_type: Used to select the core to erase. Possible values are ``CoreId.APPLICATION``
                            or ``CoreId.NETWORK``
        :type memory_type: ``CoreId``
        """
        assert memory_type in [CoreId.APPLICATION, CoreId.NETWORK]

        self._probe.erase(erase_kind=Erase.ALL, core=memory_type)
    # end def erase_firmware

    def flash_firmware(self, firmware_hex_file, no_reset=False, memory_type=CoreId.APPLICATION):
        """
        Flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str`` or ``IntelHex``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``
        :param memory_type: Used to select the core to flash. Possible values are ``CoreId.APPLICATION``
                            or ``CoreId.NETWORK``
        :type memory_type: ``CoreId``

        :return: Status
        :rtype: ``int``
        """
        assert memory_type in [CoreId.APPLICATION, CoreId.NETWORK]

        flash_hex_file = IntelHex(firmware_hex_file)
        # Create a temporary file which is going to be deleted just after the flashing
        flash_hex_file_path = "tmp_flash_file.hex"
        flash_hex_file.write_hex_file(flash_hex_file_path)

        status = None
        if self._probe is not None:
            try:
                if no_reset:
                    status = self._probe.program(firmware=flash_hex_file_path, verify=Verify.READ, core=memory_type)
                else:
                    status = self._probe.program(firmware=flash_hex_file_path, verify=Verify.READ,
                                                 reset_kind=Reset.HARD, core=memory_type)
                    # Time to let the DUT reboot
                    sleep(REBOOT_TIME)
                # end if
            except ProbeError:
                self._stdout.write(f"NRF Probe lib Debugger flashing {firmware_hex_file} failed: "
                                   f"{TracebackLogWrapper.get_exception_stack()}\n")
            finally:
                remove(flash_hex_file_path)
            # end try
        else:
            remove(flash_hex_file_path)
        # end if
        return status
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
        self.flash_firmware(firmware_hex_file, no_reset)
    # end def erase_and_flash_firmware

    def reload_file(self, firmware_hex_file=None, nvs_hex_file=None, no_reset=False):
        """
        Flash the whole target device. At least one of the two OPTIONAL hex file parameters should be not None.

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
            total_bank_size = sum(bank_size_list) * 2
            # Erase all banks
            flash_hex_file = self.remove_data_block(flash_hex_file, start_address, total_bank_size)
        # end if

        # Remove UICR address range to preserve AES NVS encryption key
        flash_hex_file = self.remove_uicr_block(flash_hex_file)

        return self.flash_firmware(flash_hex_file, no_reset)
    # end def reload_file

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

        # Remove UICR address range to preserve AES NVS encryption key
        flash_hex_file = self.remove_uicr_block(flash_hex_file)

        # Remove all range before NVS address
        flash_hex_file = self.remove_data_block(flash_hex_file, 0, self.NVS_START_ADDRESS)

        flash_hex_file.write_hex_file(flash_hex_file_path)
        status = None
        self.stop()
        if self._probe is not None:
            try:
                status = self._probe.program(firmware=flash_hex_file_path)
            finally:
                remove(flash_hex_file_path)
            # end try
        else:
            remove(flash_hex_file_path)
        # end if
        self._probe.go()

        return status
    # end def reload_nvs_no_device_reset

    def exclude_flash_cache_range(self, start_address, stop_address):
        """
        Exclude a part of the flash from the internal cache of the jlink probe.
        WARNING: calling it again remove the exclusion of the precedent call.
        Example, this code will end up only excluding UICR and not NVS::
            self.exclude_flash_cache_range(self.NVS_START_ADDRESS, self.NVS_START_ADDRESS + self.NVS_SIZE)
            self.exclude_flash_cache_range(UICR_START_ADDRESS, UICR_START_ADDRESS + UICR_GRAVITON_SIZE)
        """
        pass
    # end def exclude_flash_cache_range

    def get_rtt_address(self):
        """
        Return the address of the RTT buffer.
        """
        return self._rtt_buffer_address
    # end def get_rtt_address

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

    def remove_uicr_block(self, flash_hex_file):
        """
        Delete the UICR data block from the given binary file

        :param flash_hex_file: Firmware Hex file
        :type flash_hex_file: ``IntelHex``

        :return: Modified firmware Hex file
        :rtype: ``IntelHex``
        """
        return flash_hex_file
    # end def remove_uicr_block

    def get_mcu_type(self):
        """
        Get MCU type information

        :return: MCU type information
        :rtype: ``str|None``
        """
        if self._probe is not None:
            mcu_type = self._probe.identify()
            return mcu_type
        # end if
        return None
    # end def get_mcu_type

    def log_device_info(self):
        """
        Send Device information on console
        """
        if self._probe is not None:
            #  Get the current protection of the device.
            sys.stdout.write(f'Device protection: {self._probe.get_protection()}\n')

            mcu_info = self._probe.get_core_info()
            sys.stdout.write(f'mcu info = {mcu_info}\n')

            mcu_type = self._probe.identify()
            sys.stdout.write(f'mcu type = {mcu_type}\n')
            if mcu_type is None or not str(mcu_type).startswith(self.MCU_NAME.split('_')[0]):
                # Check of MCU type failed
                raise ValueError(f'Wrong MCU type detected: {mcu_type}')
            # end if
        # end if
    # end def log_device_info
# end class NrfProbeDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Nrf54H20ProbeDebugger(NrfProbeDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF54 TIGER MCU
    """
    MCU_NAME = 'NRF54H20_xxAA_ENGA'
    NVS_START_ADDRESS = 0X0E0AA7A0
    NVS_SIZE = 0 # 24 * 1024 # disabled to skip NVS until ready
    NVS_BANK_SIZE = [4096, 4096, 4096]

    UICR_START_ADDRESS = 0xFFF8000
    UICR_SIZE = 0x7B0
# end class Nrf54H20ProbeDebugger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
