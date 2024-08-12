#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyharness.debuggers.jlinkdebugger
:brief: Debugger using J-Link Base Compact probe
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/09/12
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import subprocess
import sys
from abc import ABC
from os import remove
from os.path import dirname
from time import sleep

from intelhex import IntelHex
from pylink.enums import JLinkInterfaces
from pylink.errors import JLinkException
from pylink.errors import JLinkReadException
from pylink.jlink import JLink
from pylink.library import Library

from pyharness.debuggers.nvsdebugger import NvsDebugger
from pylibrary.system.debugger import Debugger
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.tracebacklog import TracebackLogWrapper

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
Verbose = False
ERROR_VERBOSE = True

USE_SPEED_4000 = False
CONNECTION_SPEED = 4000 if USE_SPEED_4000 else 'auto'
CONNECTION_RETRY_SPEED = 1000

# SEGGER Identifier
SEGGER_VENDOR_ID = 0x1366
SEGGER_PRODUCT_ID = 0x0101

RTT_BUFFER_SYMBOL = '_SEGGER_RTT'
UICR_START_ADDRESS = 0x10001000
UICR_GRAVITON_SIZE = 0x308

REGISTER_SIZE = 4
# NRF52 RESETREAS register
RESETREAS_ADDRESS = 0x40000400
# HexList format   31 30 29 28 27 26 25 24 23 22 21 20 19 18 17 16 15 14 13 12 11 10  9  8  7  6  5  4  3  2  1  0
# NRF52 register    7  6  5  4  3  2  1  0 15 14 13 12 11 10  9  8 24 23 22 21 20 19 18 17 16 31 30 29 28 27 26 25
SOFT_RESET_BIT = 26  # bit 2 of byte 3
BL_APP_SELECT_BIT = 31  # bit 7 of byte 3
RECOVERY_SELECT_BIT = 30  # bit 6 of byte 3
# NRF52 GPREGRET register
GPREGRET_ADDRESS = 0x4000051C
# NRF52 GPREGRET2 register
GPREGRET2_ADDRESS = 0x40000520

# STM32 constants
# RCC reset status register (RCC_RSR) at address 0x580244D0
STM32_RST_STATUS_REG_ADDRESS = 0x580244D0
# RCC reset status register (RCC_RSR) Reset value: 0x00E80000
STM32_RST_STATUS_REG_POWER_ON_RESET_VALUE = HexList("00E80000")


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class JlinkDebugger(NvsDebugger, ABC):
    """
    Implementation of a debugger using J-link dll.
    """
    VERSION = '0.1.1'

    NVS_START_ADDRESS = None
    NVS_SIZE = None
    NVS_BANK_SIZE = None

    def __init__(self, input_dir='.', local_dir=None, debugger_number=0):
        """
        :param input_dir: input/output directory - OPTIONAL
        :type input_dir: ``str``
        :param local_dir: The configuration directory. - OPTIONAL
        :type local_dir: ``str``
        :param debugger_number: Debugger number - OPTIONAL
        :type debugger_number: ``int``
        """
        super(JlinkDebugger, self).__init__(input_dir, local_dir, debugger_number)
        self.__next__ = self

        # Initialize an instance of a J-Link dll Library with a predefined filename
        # cf existing issue: https://github.com/square/pylink/issues/183
        dllpath = '/opt/SEGGER/JLink/libjlinkarm.so'
        self.jlink_lib = Library(dllpath=dllpath)

        self._stdout = sys.stdout
        self._serial_no = 0
        self._rtt_buffer_address = None
        self._j_link = None
    # end def __init__

    def open(self, unlock_device=False, exclude_nvs_range=True, **kwargs):
        """
        Open a connection to the debugger, using previously supplied parameters.

        :param unlock_device: Unlock the device if needed before the call to connect, this will be used only for
                              nRF52 devices - OPTIONAL
        :type unlock_device: ``bool``
        :param exclude_nvs_range: Flag indicating to exclude NVS addresses in the cached range - OPTIONAL
        :type exclude_nvs_range: ``bool``
        :param kwargs: debugger specific parameters
        :type kwargs: ``any``

        :raise ``AssertionError``: If the debugger is already opened
        :raise ``JLinkException``: If an error occurs during the connection
        """
        assert self._openCount == 0, f"Cannot open a {self.__class__.__name__}  instance more than once"

        super().open(**kwargs)

        if unlock_device:
            self.unlock_target()
        # end if

        self._j_link = JLink(self.jlink_lib)
        assert (isinstance(self._j_link, JLink))
        assert (self._j_link.version >= '7.88')

        try:
            self._j_link.open(int(self._serial_no))

            # j_link.set_tif(JLinkInterfaces.SWD)
            # TypeError: 'int' object is not callable
            # => replace the function call by the following code
            # -------- set_tif workaround ------------
            interface = JLinkInterfaces.SWD
            if not ((1 << interface) & self._j_link.supported_tifs()):
                raise JLinkException('Unsupported target interface: %s' % interface)
            # end if

            # The return code here is actually *NOT* the previous set interface, it
            # is ``0`` on success, otherwise ``1``.
            # noinspection PyProtectedMember
            res = self._j_link._dll.JLINKARM_TIF_Select(interface)
            if res != 0:
                raise JLinkException('Error during SWD Interface selection: %d' % res)
            # end if
            self._j_link._tif = interface
            # -------- End of set_tif workaround -----

            try:
                self._j_link.connect(self.get_device(), speed=CONNECTION_SPEED)
            except JLinkException:
                if ERROR_VERBOSE:
                    self._stdout.write(f"JlinkDebugger connect failed, unlock device and "
                                       f"retry: {TracebackLogWrapper.get_exception_stack()}\n")
                # end if
                self.unlock_target()
                self._j_link.connect(self.get_device(), speed=CONNECTION_SPEED)
            # end try

            self._openCount += 1

            if exclude_nvs_range and self.NVS_START_ADDRESS and self.NVS_SIZE:
                self.exclude_flash_cache_range(self.NVS_START_ADDRESS, self.NVS_START_ADDRESS + self.NVS_SIZE)
            # end if
        except Exception:
            if ERROR_VERBOSE:
                self._stdout.write(f"JlinkDebugger open failed: {TracebackLogWrapper.get_exception_stack()}\n")
            # end if
            if self._j_link is not None:
                self._j_link.close()
                del self._j_link
                self._j_link = None
            # end if
            raise
        # end try
    # end def open

    def close(self):
        """
        Close a connection to the debugger.
        """
        if self._openCount == 0:
            return
        # end if

        super(JlinkDebugger, self).close()

        if self._openCount == 1 and self._j_link is not None:
            self._j_link.close()
            del self._j_link
            self._j_link = None
        # end if

        if self._openCount > 0:
            self._openCount -= 1
        # end if
    # end def close

    def reset(self, soft_reset=True, skip_current_breakpoint=True):
        """
        Reset the j-link debugger.
        Reset behavior:
         - Soft reset: CPU, Peripherals	and GPIO reset
         - Emulated power on reset (NRF52 Family only): idem 'Soft reset' plus cleanup retained registers and clear soft
         reset bit in 'RESETREAS' register.

        :param soft_reset: flag to select between a soft reset and an emulated power on reset - OPTIONAL
        :type soft_reset: ``bool``
        :param skip_current_breakpoint: flag to stop on / skip (default) the current breakpoint. - OPTIONAL
        :type skip_current_breakpoint: ``bool``

        :return: Status
        :rtype: ``int``

        :raise ``TypeError``: If the reset type is not supported
        :raise ``AssertionError``: If soft reset bit or retained registers are not cleared
        """
        if self._j_link is not None and self._j_link.opened():
            if soft_reset:
                # Soft reset
                self._j_link.reset(halt=False)
            elif self.MCU_NAME.startswith('NRF52'):
                # Emulate a power-on-reset - NRF52 Family specific
                self._j_link.reset(halt=True)
                # Get NRF52 'Reset reason' register
                reset_reason_register = HexList(self._j_link.memory_read(RESETREAS_ADDRESS, REGISTER_SIZE))
                # Reset from soft reset detected ?
                if reset_reason_register.testBit(SOFT_RESET_BIT):
                    # A field is cleared by writing '1' to it
                    self._j_link.memory_write(RESETREAS_ADDRESS, HexList(Numeral(1 << SOFT_RESET_BIT, REGISTER_SIZE)))
                    # Check soft reset bit has been cleared
                    reset_reason_register_check = HexList(self._j_link.memory_read(RESETREAS_ADDRESS, REGISTER_SIZE))
                    assert (reset_reason_register_check.testBit(SOFT_RESET_BIT) is False)
                    # Clean-up retained registers
                    # GPREGRET	- General purpose retention register
                    cleared_register = HexList("00"*REGISTER_SIZE)
                    self._j_link.memory_write(GPREGRET_ADDRESS, cleared_register)
                    retention_register_check = HexList(self._j_link.memory_read(GPREGRET_ADDRESS, REGISTER_SIZE))
                    assert (retention_register_check == cleared_register)
                    # GPREGRET2	- General purpose retention register
                    self._j_link.memory_write(GPREGRET2_ADDRESS, cleared_register)
                    retention_register2_check = HexList(self._j_link.memory_read(GPREGRET2_ADDRESS, REGISTER_SIZE))
                    assert (retention_register2_check == cleared_register)
                    # Warning: WDT ? Watchdog timer not reset
                # end if
                # Add a 80ms delay letting the LS2 receiver detect and report the disconnection
                sleep(.08)
                self._j_link.restart(skip_breakpoints=skip_current_breakpoint)
            elif self.MCU_NAME.startswith(('STM32', 'LEXEND')):
                self._j_link.reset(halt=False)
            else:
                raise TypeError('Unsupported reset type')
            # end if
        # end if
        return 0
    # end def reset

    def run(self, skip_current_breakpoint=True):
        """
        Restarts the CPU core if it was previously halted.

        :param skip_current_breakpoint: flag to stop on / skip (default) the current breakpoint. - OPTIONAL
        :type skip_current_breakpoint: ``bool``
        """
        if self._j_link is not None and self._j_link.opened() and self._j_link.halted():
            self._j_link.restart(skip_breakpoints=skip_current_breakpoint)
        # end if

        if Verbose:
            self._stdout.write('RUN of the simulator')
        # end if
    # end def run

    def isRunning(self):
        """
        Indicate if the CPU is halted or not

        :return: Flag indicating if the CPU is halted or not.
        :rtype: ``bool``
        """
        if self._j_link is not None and self._j_link.opened() and not self._j_link.halted():
            if Verbose:
                self._stdout.write('simulator is RUNNING')
            # end if
            return True
        else:
            if Verbose:
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
        if self._j_link is not None and self._j_link.opened() and not self._j_link.halted():
            self._j_link.halt()
        # end if

        if Verbose:
            self._stdout.write('STOP of the simulator')
        # end if
        return 0
    # end def stop

    # noinspection PyPep8Naming
    # noinspection PyShadowingBuiltins
    def loadCoverage(self, filePath, format=Debugger.FORMAT_COMMON):    # @ReservedAssignment pylint:disable=W0622,W5508
        """
        @copydoc pylibrary.system.debugger.Debugger.loadCoverage
        """
        raise NotImplementedError
    # end def loadCoverage

    # noinspection PyPep8Naming
    # noinspection PyShadowingBuiltins
    def saveCoverage(self, filePath, format=Debugger.FORMAT_COMMON):    # @ReservedAssignment pylint:disable=W0622,W5508
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
        name = 'J-Link Debugger'
        if Verbose:
            self._stdout.write(name)
        # end if
        return name
    # end def __str__

    def getVersion(self):
        """
        Obtain the version of this debugger.

        :return: The debugger version
        :rtype: ``str``
        """
        return self.VERSION
    # end def getVersion

    # noinspection PyPep8Naming
    def getRegisters(self, registersList):                              # pylint:disable=W0613,W5508
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
    def readMemory(self, addressOrLabel, length, memoryType=None):
        """
        @copydoc pylibrary.system.debugger.Debugger.readMemory

        :param addressOrLabel: The address or label of the memory to read
        :type addressOrLabel: ``int``
        :param length: The length of the memory to read
        :type length: ``int``
        :param memoryType: The type of memory to read - OPTIONAL
        :type memoryType: ``str | None``

        :return: The memory content
        :rtype: ``HexList``

        :raise ``AssertionError``: If the addressOrLabel is not an integer
        """
        assert isinstance(addressOrLabel, int), TypeError('Should be int instead')

        try:
            buffer = self._j_link.memory_read(addr=addressOrLabel, num_units=length)
        except (JLinkReadException, ValueError):
            if ERROR_VERBOSE:
                self._stdout.write(f"JlinkDebugger readMemory failed, retry with halting the device: "
                                   f"{TracebackLogWrapper.get_exception_stack()}\n")
            # end if
            # JLinkReadException or ValueError: Invalid error code
            self._j_link.reset(halt=True)
            buffer = self._j_link.memory_read(addr=addressOrLabel, num_units=length)
            self._j_link.reset(halt=False)

            # TODO find away to tell the upper layers that a reset has been performed
        # end try
        return HexList(buffer)
    # end def readMemory

    # noinspection PyPep8Naming
    def writeMemory(self, addressOrLabel, data, memoryType=None):
        """
        @copydoc corepython.system.debugger.Debugger.writeMemory

        :param addressOrLabel: The address or label of the memory to write
        :type addressOrLabel: ``int``
        :param data: The data to write
        :type data: ``HexList``
        :param memoryType: The type of memory to write - OPTIONAL
        :type memoryType: ``str | None``

        :return: Status
        :rtype: ``int``

        :raise ``RuntimeError``: If the memory write fails
        """
        address = self.getAddress(addressOrLabel, memoryType)
        if self._j_link is not None and self._j_link.opened():
            return self._j_link.memory_write(addr=address, data=data)
        else:
            raise RuntimeError("Unable to write memory")
        # end if
    # end def writeMemory

    def erase_firmware(self):
        """
        Erase firmware.
        """
        self._j_link.reset(halt=True)
        self._j_link.erase()
    # end def erase_firmware

    def flash_firmware(self, firmware_hex_file, no_reset=False):
        """
        Flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str`` or ``IntelHex``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``

        :return: Status
        :rtype: ``int``
        """
        flash_hex_file = IntelHex(firmware_hex_file)
        # Create a temporary file which is going to be deleted just after the flashing
        flash_hex_file_path = "tmp_flash_file.hex"
        flash_hex_file.write_hex_file(flash_hex_file_path)

        status = None
        if self._j_link is not None and self._j_link.opened():
            try:
                self._j_link.reset(halt=True)
                status = self._j_link.flash_file(path=flash_hex_file_path, addr=0x0, on_progress=None, power_on=False)
                if not no_reset:
                    self._j_link.reset(halt=False)
                elif self.isRunning():
                    self._j_link.reset(halt=True)
                # end if
            except JLinkException:
                if ERROR_VERBOSE:
                    self._stdout.write(f"JlinkDebugger flashing {firmware_hex_file} failed, retry: "
                                       f"{TracebackLogWrapper.get_exception_stack()}\n")
                # end if
                self._j_link.reset(halt=True)
                # Retry flashing the device
                status = self._j_link.flash_file(path=flash_hex_file_path, addr=0x0, on_progress=None, power_on=False)
                if not no_reset:
                    self._j_link.reset(halt=False)
                elif self.isRunning():
                    self._j_link.reset(halt=True)
                # end if
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

        :raise ``AssertionError``: If the NVS is not erased
        """
        self.erase_firmware()
        nvs = self.readMemory(addressOrLabel=self.NVS_START_ADDRESS, length=self.NVS_SIZE)
        assert nvs == HexList("FF" * self.NVS_SIZE), "NVS should be erased"
        self.flash_firmware(firmware_hex_file, no_reset)
    # end def erase_and_flash_firmware

    def reload_file(self, firmware_hex_file=None, nvs_hex_file=None, no_reset=False):
        """
        Flashes the whole target device. At least one of the two OPTIONAL hex file parameters should be not None.

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

        :raise ``AssertionError``: If firmware_hex_file and nvs_hex_file are None
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

        :return: Status
        :rtype: ``int``
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
        if self._j_link is not None and self._j_link.opened():
            try:
                status = self._j_link.flash_file(path=flash_hex_file_path, addr=0x0, on_progress=None, power_on=False)
            finally:
                remove(flash_hex_file_path)
            # end try
        else:
            remove(flash_hex_file_path)
        # end if
        self.run()

        return status
    # end def reload_nvs_no_device_reset

    def exclude_flash_cache_range(self, start_address, stop_address):
        """
        Exclude a part of the flash from the internal cache of the jlink probe.
        WARNING: calling it again remove the exclusion of the precedent call.
        Example, this code will end up only excluding UICR and not NVS::
            self.exclude_flash_cache_range(self.NVS_START_ADDRESS, self.NVS_START_ADDRESS + self.NVS_SIZE)
            self.exclude_flash_cache_range(UICR_START_ADDRESS, UICR_START_ADDRESS + UICR_GRAVITON_SIZE)

        :param start_address: Start address of the range to exclude
        :type start_address: ``int``
        :param stop_address: Stop address of the range to exclude
        :type stop_address: ``int``
        """
        self._j_link.exec_command(f"ExcludeFlashCacheRange {hex(start_address)}-{hex(stop_address)}")
    # end def exclude_flash_cache_range

    def get_jlink(self):
        """
        Return the JLink instance.

        :return: JLink instance
        :rtype: ``JLink``
        """
        return self._j_link
    # end def get_jlink

    def get_rtt_address(self):
        """
        Return the address of the RTT buffer.

        :return: Address of the RTT buffer
        :rtype: ``int``
        """
        return self._rtt_buffer_address
    # end def get_rtt_address

    def set_application_bit(self, no_reset=False):
        """
        Select the reboot mode of the firmware.
        Context: NRF52 Firmwares leverage the GPREGRET register to store Bootloader / Application reboot mode.

        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``
        """
        if self.MCU_NAME.startswith('NRF52'):
            self.stop()
            loop_count = 0
            gpregret_register = HexList(self._j_link.memory_read(GPREGRET_ADDRESS, REGISTER_SIZE))
            while gpregret_register.testBit(BL_APP_SELECT_BIT) and loop_count < 3:
                gpregret_register.clearBit(BL_APP_SELECT_BIT)
                gpregret_register.clearBit(RECOVERY_SELECT_BIT)
                self._j_link.memory_write(GPREGRET_ADDRESS, gpregret_register)

                gpregret_register = HexList(self._j_link.memory_read(GPREGRET_ADDRESS, REGISTER_SIZE))
                if gpregret_register.testBit(BL_APP_SELECT_BIT):
                    self._stdout.write(f"application bit not set (loop count = {loop_count})\n")
                    self._j_link.reset(halt=True)
                # end if
                loop_count += 1
            # end while
            if not no_reset:
                self._j_link.reset(halt=False)
            # end if
        # end if
    # end def set_application_bit

    def unlock_target(self):
        """
        Unlock the device. This will only be performed for nRF52 devices.

        :raise ``RuntimeError``: If the unlocking fails
        """
        if self.MCU_NAME.startswith('NRF52'):
            cmd = f"/opt/SEGGER/JLink/JLinkExe -device nRF52 -SelectEmuBySn {self._serial_no} -if SWD -speed " \
                  f"{CONNECTION_SPEED} -CommandFile {dirname(__file__)}/recover.jlink"
            result = subprocess.run(cmd, shell=True, capture_output=True)
            output = result.stdout.decode("utf-8")
            if result.returncode != 0 or "Connecting to J-Link via USB...FAILED: Cannot connect to J-Link." in output:
                raise RuntimeError('Unlocking device FAILED:\n' + output)
            # end if
        elif self.MCU_NAME.startswith('STM32'):
            cmd = f"/opt/SEGGER/JLink/JLinkExe -device {self.MCU_NAME} -SelectEmuBySn {self._serial_no} -if SWD " \
                  f"-speed {CONNECTION_SPEED} -CommandFile {dirname(__file__)}/stm_recover.jlink"
            result = subprocess.run(cmd, shell=True, capture_output=True)
            output = result.stdout.decode("utf-8")
            if result.returncode != 0 or "Connecting to J-Link via USB...FAILED: Cannot connect to J-Link." in output:
                raise RuntimeError('Unlocking device FAILED:\n' + output)
            # end if
        # end if
    # end def unlock_target

    def add_breakpoint(self, address):
        """
        Add a breakpoint to the debugger

        :param address: The address at which to set the breakpoint
        :type address: ``int``

        :return: An integer specifying the trace event handle
        :rtype: ``int``

        :raise ``AssertionError``: If the new breakpoint count is not equal to the initial count + 1
        """
        initial_count = self._j_link.num_active_breakpoints()
        breakpoint_id = self._j_link.hardware_breakpoint_set(address, thumb=True)
        next_count = self._j_link.num_active_breakpoints()
        assert next_count == initial_count + 1
        breakpoint_info = self._j_link.breakpoint_info(handle=breakpoint_id)
        return breakpoint_info.Handle
    # end def add_breakpoint

    def clear_breakpoints(self):
        """
        Clear all breakpoints
        """
        self._j_link.breakpoint_clear_all()
    # end def clear_breakpoints

    def remove_uicr_block(self, flash_hex_file):
        """
        Delete the UICR data block from the given binary file

        :param flash_hex_file: Firmware Hex file
        :type flash_hex_file: ``IntelHex``

        :return: Modified firmware Hex file
        :rtype: ``IntelHex``
        """
        if self.MCU_NAME.startswith('NRF52'):
            # Remove UICR address range to preserve AES NVS encryption key
            return self.remove_data_block(flash_hex_file, UICR_START_ADDRESS, UICR_GRAVITON_SIZE)
        else:
            return flash_hex_file
        # end if
    # end def remove_uicr_block

    def get_pc_register_index(self):
        """
        Get the index of the PC register

        :return: Index of the PC register
        :rtype: ``int``
        """
        for register_index in self._j_link.register_list():
            if "PC" in self._j_link.register_name(register_index=register_index):
                return register_index
            # end if
        # end for
    # end def get_pc_register_index

    def get_pc_register_value(self, pc_reg_idx):
        """
        Get the value of the PC register

        :param pc_reg_idx: Index of the PC register
        :type pc_reg_idx: ``int``

        :return: Value of the PC register
        :rtype: ``int``
        """
        self._j_link.halt()
        pc_reg_val = self._j_link.register_read(register_index=pc_reg_idx)
        self._j_link.restart()
        return pc_reg_val
    # end def get_pc_register_value
# end class JlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class GravitonJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Graviton MCU.
    """
    MCU_NAME = 'NRF52840_XXAA'
    NVS_START_ADDRESS = 0xFA000
    NVS_SIZE = 24 * 1024
    NVS_BANK_SIZE = [4096, 4096, 4096]
# end class GravitonJlinkDebugger


# noqa is used to suppress warnings about incomplete implementation of methods from a parent class.
class Graviton4Zones64KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Graviton MCU, 64K NVS and 4 distinct zones
    
    Zone0 8K  "Factory settings"
    Zone1 8K  "Pairing info"
    Zone2 40K "Bulk"
    Zone3 8K  "Common"
    """
    MCU_NAME = 'NRF52840_XXAA'
    NVS_START_ADDRESS = 0xF0000
    NVS_SIZE = 64 * 1024
    NVS_BANK_SIZE = [4096, 4096, 20480, 4096]
# end class Graviton4Zones64KJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class QuarkJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Quark MCU.
    """
    MCU_NAME = 'NRF52832_XXAA'
    NVS_START_ADDRESS = 0x7E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
# end class QuarkJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class QuarkMultiZoneJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Quark MCU enabling the NVS multi zone option.
    """
    MCU_NAME = 'NRF52832_XXAA'
    NVS_START_ADDRESS = 0x76000
    NVS_SIZE = 40 * 1024
    NVS_BANK_SIZE = [4096, 4096, 8192, 4096]
# end class QuarkMultiZoneJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Quark256JlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Quark256 MCU.
    """
    MCU_NAME = 'NRF52832_XXAB'
    NVS_START_ADDRESS = 0x3E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
# end class Quark256JlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class GluonJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Gluon MCU.
    """
    MCU_NAME = 'NRF52810_XXAA'
    NVS_START_ADDRESS = 0x2E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
# end class GluonJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class CommonMesonJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Meson MCU.
    """
    def erase_firmware(self):
        """
        Erase firmware.
        """
        was_open = False
        try:
            if self.isOpen():
                was_open = True
                self.close()
            # end if
            self.unlock_target()
        finally:
            if was_open:
                self.open()
            # end if
        # end try
    # end def erase_firmware
# end class CommonMesonJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class DeviceMesonJlinkDebugger(CommonMesonJlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Meson MCU in device.
    """
    MCU_NAME = 'NRF52820_XXAA'
    NVS_START_ADDRESS = 0x3E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
# end class DeviceMesonJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Hadron3Zones24KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU, 24K NVS and 3 distinct zones (i.e. PWS devices)
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x7A000
    NVS_SIZE = 24 * 1024
    NVS_BANK_SIZE = [4096, 4096, 4096]
# end class Hadron3Zones24KJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Hadron4Zones40KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU in device.
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x76000
    NVS_SIZE = 40 * 1024
    NVS_BANK_SIZE = [4096, 4096, 8192, 4096]
# end class Hadron4Zones40KJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Hadron5Zones64KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU, 64K NVS and 5 distinct zones
    Zone0 8K  "Factory settings"
    Zone1 8K  "Pairing info"
    Zone2 32K "Bulk"
    Zone3 8K  "Nervous stuff"
    Zone4 8K  "Common"
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x70000
    NVS_SIZE = 64 * 1024
    NVS_BANK_SIZE = [4096, 4096, 16384, 4096, 4096]
# end class Hadron5Zones64KJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Hadron4Zones64KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU, 64K NVS and 4 distinct zones
    Zone0 8K  "Factory settings"
    Zone1 8K  "Pairing info"
    Zone2 40K "Bulk"
    Zone3 8K  "Common"
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x70000
    NVS_SIZE = 64 * 1024
    NVS_BANK_SIZE = [4096, 4096, 20480, 4096]
# end class Hadron4Zones64KJlinkDebugger


class Hadron4Zones104KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU, 104K NVS and 4 distinct zones
    Zone0 8K  "Factory settings"
    Zone1 8K  "Pairing info"
    Zone2 80K "Bulk"
    Zone3 8K  "Common"
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x66000
    NVS_SIZE = 104 * 1024
    NVS_BANK_SIZE = [4096, 4096, 40960, 4096]
# end class Hadron4Zones104KJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class Hadron1Zone8KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU, 8K NVS and 1 zone.
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x7E000
    NVS_SIZE = 8 * 1024
    NVS_BANK_SIZE = 4 * 1024
# end class Hadron1Zone8KJlinkDebugger

# noqa is used to remove waning about not having all methods from parent class implemented
class Hadron1Zone24KJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Hadron MCU, 8K NVS and 1 zone.
    """
    MCU_NAME = 'NRF52833_XXAA'
    NVS_START_ADDRESS = 0x7A000
    NVS_SIZE = 24 * 1024
    NVS_BANK_SIZE = 12 * 1024
# end class Hadron1Zone24KJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class ReceiverMesonJlinkDebugger(CommonMesonJlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Meson MCU in receiver
    """
    MCU_NAME = 'NRF52820_XXAA'
    NVS_START_ADDRESS = 0x3C000
    NVS_SIZE = 16 * 1024
    NVS_BANK_SIZE = 8 * 1024
# end class ReceiverMesonJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class MezzyOnGravitonJlinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the NRF52 Meson MCU.
    """
    MCU_NAME = 'NRF52840_XXAA'
    NVS_START_ADDRESS = 0x3C000
    NVS_SIZE = 16 * 1024
    NVS_BANK_SIZE = 8 * 1024
# end class MezzyOnGravitonJlinkDebugger


# noqa is used to remove waning about not having all methods from parent class implemented
class STM32F723IEJLinkDebugger(JlinkDebugger):  # noqa
    """
    Implementation of a debugger configured for the STM32F723IE MCU, companion MCU on Savituck.
    """
    MCU_NAME = 'STM32F723IE'

    FMM_FLASH_SIZE = 256 * 1024
    FMM_FLASH_START_ADDR = 0x08000000
    FMM_FLASH_END_ADDR = FMM_FLASH_START_ADDR + FMM_FLASH_SIZE - 1
    FMM_BOOT_SIZE = 128 * 1024
    FWW_BOOT_START_ADDR = FMM_FLASH_START_ADDR
    FMM_APP_START_ADDR = FWW_BOOT_START_ADDR + FMM_BOOT_SIZE
    FMM_APP_END_ADDR = FMM_FLASH_END_ADDR

    # Non-Volatile Flash storage for Bootloader, since real EEPROM is not supported
    FMM_BOOT_FLASH_NVS_SECTOR = 1
    FMM_BOOT_FLASH_NVS_SECTOR_SIZE = 16 * 1024
    FMM_BOOT_FLASH_NVS_SIZE = FMM_BOOT_FLASH_NVS_SECTOR_SIZE
    FMM_BOOT_FLASH_NVS_START_ADDR = FWW_BOOT_START_ADDR + FMM_BOOT_FLASH_NVS_SECTOR * FMM_BOOT_FLASH_NVS_SECTOR_SIZE
    FMM_BOOT_FLASH_NVS_END_ADDR = FMM_BOOT_FLASH_NVS_START_ADDR + FMM_BOOT_FLASH_NVS_SIZE - 1
    FMM_BOOT_FLASH_NVS_LIMIT_ADDR = FMM_BOOT_FLASH_NVS_START_ADDR + FMM_BOOT_FLASH_NVS_SIZE

    # RAM
    FMM_TOTAL_RAM_SIZE = 256 * 1024
    FMM_RAM_START_ADDR = 0x20000000
    FMM_NOINIT_SIZE = 4
    FMM_RAM_SIZE = FMM_TOTAL_RAM_SIZE - FMM_NOINIT_SIZE
    FMM_NOINIT_START_ADDR = FMM_RAM_START_ADDR + FMM_RAM_SIZE

    # CRC
    FMM_CRC_SIZE = 4
    FMM_CRC_STORE_ADDR = FMM_APP_END_ADDR - FMM_CRC_SIZE + 1

    DFU_REQUESTED = HexList("55555555")
    DFU_NOT_REQUESTED = HexList("00000000")
# end class STM32F723IEJLinkDebugger


class STM32F072CBJlinkDebugger(JlinkDebugger):
    """
    Implementation of a debugger configured for the STM32F072CB
    """
    MCU_NAME = 'STM32F072CB'

    NVS_START_ADDRESS = 0x8004000
    NVS_SIZE = 28 * 1024
    NVS_BANK_SIZE = 2 * 1024
# end class STM32F072CBJlinkDebugger


class STM32H7B0IBJLinkDebugger(JlinkDebugger):
    """
    Implementation of a debugger configured for the STM32H7B0IB
    """
    MCU_NAME = 'STM32H7B0IB'

    NVS_START_ADDRESS = 0x0801C000
    NVS_SIZE = 0x4000
    SECURE_BLOCK_START_ADDRESS = 0x0801A000
    NVS_SECURE_SIZE = 0x2000
    NVS_BANK_SIZE = [0x2000, 0x2000]
# end class STM32H7B0IBJLinkDebugger


class STM32L052JLinkDebugger(JlinkDebugger):
    """
    Implementation of a debugger configured for the STM32L052
    """
    MCU_NAME = 'STM32L052C8'

    NVS_START_ADDRESS = 0x08080000
    NVS_SIZE = 2 * 1024
    NVS_BANK_SIZE = 2 * 1024

    def erase_and_flash_firmware(self, firmware_hex_file, no_reset=False):
        """
        Erase and flash firmware.

        :param firmware_hex_file: Hex file of the firmware to load
        :type firmware_hex_file: ``str`` or ``IntelHex``
        :param no_reset: If True, the device will not be restarted at the end of the method (therefore it will be
                         halted) - OPTIONAL
        :type no_reset: ``bool``

        :raise ``AssertionError``: If the NVS is not erased
        """
        self.unlock_target()
        self.erase_firmware()
        nvs = self.readMemory(addressOrLabel=self.NVS_START_ADDRESS, length=self.NVS_SIZE)
        assert nvs == HexList("00" * self.NVS_SIZE), "NVS should be erased"
        self.flash_firmware(firmware_hex_file, no_reset)
    # end def erase_and_flash_firmware
# end class STM32L052JLinkDebugger


class LexendJLinkDebugger(STM32H7B0IBJLinkDebugger):
    """
    Implementation of a debugger configured for the specific configuration of Lexend with STM32H7B0IB and external
    memory
    """

    EXTERNAL_FLASH_BASE_ADDRESS = 0x90000000
    # Time in seconds to wait after device reset to complete the USB enumeration
    WAIT_AFTER_RESET = 0.7

    def writeMemory(self, addressOrLabel, data, memoryType=None):
        # See ``JlinkDebugger.writeMemory``
        address = self.getAddress(addressOrLabel, memoryType)
        if address >= self.EXTERNAL_FLASH_BASE_ADDRESS:
            with self.opened_with_mcu_name(mcu_name='LEXEND'):
                super().writeMemory(addressOrLabel, data, memoryType)
            # end with
        else:
            super().writeMemory(addressOrLabel, data, memoryType)
        # end if
    # end def writeMemory

    def erase_firmware(self):
        # See ``JlinkDebugger.erase_firmware``
        with self.opened_with_mcu_name(mcu_name='LEXEND'):
            self._j_link.exec_command("EnableEraseAllFlashBanks")
            super().erase_firmware()
        # end with
        super().erase_firmware()
    # end def erase_firmware

    def flash_firmware(self, firmware_hex_file, no_reset=False):
        # See ``JlinkDebugger.flash_firmware``
        if firmware_hex_file.minaddr() >= self.EXTERNAL_FLASH_BASE_ADDRESS:
            with self.opened_with_mcu_name(mcu_name='LEXEND'):
                super().flash_firmware(firmware_hex_file=firmware_hex_file, no_reset=no_reset)
                sleep(self.WAIT_AFTER_RESET)
            # end with
        elif firmware_hex_file.maxaddr() < self.EXTERNAL_FLASH_BASE_ADDRESS:
            super().flash_firmware(firmware_hex_file=firmware_hex_file, no_reset=no_reset)
        else:
            ext_flash = IntelHex()
            int_flash = IntelHex()
            for addr in firmware_hex_file.addresses():
                if addr >= self.EXTERNAL_FLASH_BASE_ADDRESS:
                    ext_flash[addr] = firmware_hex_file[addr]
                else:
                    int_flash[addr] = firmware_hex_file[addr]
                # end if
            # end for
            super().flash_firmware(firmware_hex_file=int_flash, no_reset=False)
            sleep(self.WAIT_AFTER_RESET)
            with self.opened_with_mcu_name(mcu_name='LEXEND'):
                super().flash_firmware(firmware_hex_file=ext_flash, no_reset=no_reset)
                sleep(self.WAIT_AFTER_RESET)
            # end with
        # end if
    # end def flash_firmware
# end class LexendJLinkDebugger


def jlink_predicate(debugger):
    """
    Predicate for J-Link Debugger

    :param debugger: Debugger instance
    :type debugger: ``Debugger``

    :return: True if the target is the expected
    :rtype: ``bool``
    """
    debugger_tmp = debugger
    while hasattr(debugger_tmp, 'next'):
        debugger_tmp = debugger_tmp.__next__
    # end while
    return isinstance(debugger_tmp, JlinkDebugger)
# end def jlink_predicate

# noqa is used to remove waning about not having all methods from parent class implemented
class FakeDebugger(Debugger):  # noqa
    """
    Implementation of a fake debugger to reserve the first index to device target.
    """
    VERSION = '0.0.1'
    MCU_NAME = 'FakeDebugger'
    NVS_SIZE = 0

    def __init__(self, input_dir='.', local_dir=None, debugger_number=0):
        """
        :param input_dir: input/output directory - OPTIONAL
        :type input_dir: ``str``
        :param local_dir: The configuration directory. - OPTIONAL
        :type local_dir: ``str``
        :param debugger_number: Debugger number - OPTIONAL
        :type debugger_number: ``int``
        """
        super().__init__(input_dir, local_dir, debugger_number)
        self.__next__ = self
    # end def __init__

    def __str__(self):
        """
        Retrieve debugger's name

        :return: debugger name
        :rtype: ``str``
        """
        name = 'Fake Debugger'
        return name
    # end def __str__

    def getVersion(self):
        """
        Obtain the version of this debugger.

        :return: The debugger version
        :rtype: ``str``
        """
        return self.VERSION
    # end def getVersion

    def open(self, **kwargs):
        """
        Open a connection to the debugger, using previously supplied parameters.

        :param kwargs: debugger specific parameters
        :type kwargs: ``dict``
        """
        pass
    # end def open

    def close(self):
        """
        Close the fake debugger connection.
        """
        pass
    # end def close

    def reset(self, **kwargs):
        """
        Reset the fake debugger.

        :param kwargs: debugger specific parameters
        :type kwargs: ``dict``

        :return: Status
        :rtype: ``int``
        """
        return 0
    # end def reset
# end class FakeDebugger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
