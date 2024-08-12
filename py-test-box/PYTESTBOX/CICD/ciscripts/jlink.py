# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
@package ciscripts.jlink

@brief  Python interface for the SEGGER J-Link.
https://github.com/square/pylink

@author christophe Roquebert

@date   2019/03/29
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import subprocess
import sys
from argparse import ArgumentParser
from os import path
from os import remove
from os.path import isfile
from time import sleep

from intelhex import IntelHex
from pylink import JLinkConnectInfo
from pylink import JLinkHost
from pylink.enums import JLinkEraseErrors
from pylink.enums import JLinkInterfaces
from pylink.errors import JLinkEraseException
from pylink.errors import JLinkException
from pylink.errors import JLinkFlashException
from pylink.jlink import JLink
from pylink.library import Library

FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("CICD")]
PYLIBRARY_DIR = path.join(WS_DIR, "LIBS", "PYLIBRARY")
if PYLIBRARY_DIR not in sys.path:
    sys.path.insert(0, PYLIBRARY_DIR)
# end if
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.config import ConfigParser


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
# NRF52 GPREGRET register
GPREGRET_ADDRESS = 0x4000051C
GPREGRET_SIZE = 4
BL_APP_SELECT_BIT = 31

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
# J-Link configuration
# Product: J-Link OB-SAM3U128-V2-NordicSem V
# QUARK SN: 682770194
# GLUON SN: 682248056
# GRAVITON SN: 683589752
# Max SWO speed [kHz]: 12000

# Devices:
# - QUARK: NRF52810_xxAA
# - GLUON: NRF52832_xxAA
# - NRF52832_xxBB
# - GRAVITON: NRF52840_xxAA


class Flasher(object):
    """
    A program that flash a new firmware into a platform DEV board.
    """
    VERSION = '0.1.0.0'

    # SEGGER Identifier
    SEGGER_VENDOR_ID = 0x1366
    # Debugger ini file: key definition
    _SECTION_CONNECTION = 'CONNECTION'
    _KEY_SERIAL_NO = 'serial_no_'

    PLATFORM_TO_UNLOCK = ['MESON', 'HADRON', 'HADRON_GAMING', 'STM32L052C8']

    def __init__(self, stdout, stderr):
        """
        Constructor and main program entry point

        @param  stdout [in] (stream) The standard output stream
        @param  stderr [in] (stream) The standard error stream
        """
        self._stdout = stdout
        self._stderr = stderr
        self.verbose = False
        self.serial_no = 0
        self.platform_name = ''
        self.firmware_path = ''
        self._parser = None
        self.other_file_path = None
        self.nvs_path = None
        self.erase_chip = None
        self.debugger_file = None
        self.target = ''
        self.parse_args()
        self.run()
    # end def __init__

    def get_parser(self):
        """
        Get the ArgumentParser instance

        @return (ArgumentParser) ArgumentParser instance
        """
        if self._parser is None:
            parser = ArgumentParser()
            parser.add_argument('--version', action='version', version=self.VERSION)
            parser.add_argument('-v', '--verbose', dest='verbose', help='verbose output', default=False,
                                action='store_true')
            parser.add_argument('-f', '--firmware_path', dest='firmware_path', default=None,
                                metavar='FIRMWARE', help='Firmware file path')
            parser.add_argument('-p', '--platform_name', dest='platform_name', default='GRAVITON',
                                metavar='PLATFORM', help='Platform DEV board name',
                                choices=[
                                    'HADRON',
                                    'HADRON_GAMING',
                                    'GLUON',
                                    'GRAVITON',
                                    'MESON',
                                    'QUARK',
                                    'QUARK256',
                                    'STM32F0',
                                    'STM32L100',
                                    'STM32H7B0IB',
                                    'STM32F072CB',
                                    'STM32L052C8',
                                    'LEXEND',
                                ])
            parser.add_argument('-s', '--serial_no', dest='serial_no', default=None, metavar='SERIAL_NO',
                                type=int, help='Platform DEV board serial number')
            parser.add_argument('-m', '--merge', dest='other_file_path', default=None,
                                metavar='merge_files', help='Non-volatile image file path')
            parser.add_argument('-n', '--nvs_path', dest='nvs_path', default=None, metavar='NVS',
                                help='Non-volatile image file path')
            parser.add_argument('-e', '--erase-chip', dest='erase_chip', default=False,
                                action='store_true', help='Perform a full chip erase')
            parser.add_argument('-t', '--target', dest='target', default='DEVICE1', metavar='TARGET',
                                help='Helper to find Segger board serial number')
            parser.add_argument('-d', '--debugger_file', dest='debugger_file', default=None,
                                metavar='DEBUGGER', help='Helper to configure Segger board serial number')

            parser.epilog = """
Examples:
  -f //.../xxx.hex -p GRAVITON -s 683589752
or
  --firmware_path //inca.logitech.com/.../graviton.hex  # .hex file path
  --platform_name GRAVITON                              # GRAVITON / QUARK / GLUON...
  --serial_no 683589752                                 # Unique SN of the DEV Board
  --nvs-path  /path/to/nvs.hex                          # Path of a hex file used to initialize the nvs
  --erase-chip                                          # Erase full chip, not only the pages that are written.
  --target DEVICE1                                      # DEVICE1 / RECEIVER / DEVICE2
  --debugger_file debugger.ini                          # Debugger configuration file
"""
            self._parser = parser
        # end if

        return self._parser
    # end def get_parser

    parser = property(get_parser)

    def parse_args(self):
        """
        Parses the program arguments
        """
        parser = self.get_parser()
        args = parser.parse_args()

        # Iterate over the args.
        self.verbose = args.verbose
        self.erase_chip = args.erase_chip
        self.firmware_path = args.firmware_path
        self.platform_name = args.platform_name
        self.target = args.target
        self.other_file_path = args.other_file_path
        self.nvs_path = args.nvs_path
        self.serial_no = None
        self.debugger_file = args.debugger_file

        if args.serial_no:
            self.serial_no = args.serial_no
        elif args.debugger_file is not None:
            config = ConfigParser()
            file_path = self.debugger_file
            if isfile(file_path):
                config.read([file_path])
            # end if
            if self.target == 'DEVICE1':
                self.serial_no = config.get(self._SECTION_CONNECTION, '%s%d' % (self._KEY_SERIAL_NO, 0))
            elif self.target == 'RECEIVER':
                self.serial_no = config.get(self._SECTION_CONNECTION, '%s%d' % (self._KEY_SERIAL_NO, 1))
            elif self.target == 'DEVICE2':
                self.serial_no = config.get(self._SECTION_CONNECTION, '%s%d' % (self._KEY_SERIAL_NO, 2))
            # end if
        elif sys.platform == 'linux':
            # Try to guess a possible J-Link match using SEGGER Vendor Id
            segger_vid = f'{self.SEGGER_VENDOR_ID:x}'
            # lsusb -v -d 1366: | grep -oP 'iSerial +[0-9] \K[0-9]+'
            # run() returns a CompletedProcess object if it was successful
            # errors in the created process are raised here too
            try:
                completed_process = subprocess.run(
                    f'lsusb -v -d {segger_vid}: | grep -oP "iSerial +[0-9] \K[0-9]+"',
                    shell=True, check=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"command ({e.cmd}) return with error (code {e.returncode}): {e.output}")
            # end try
            assert completed_process.returncode == 0
            number_list = completed_process.stdout.rstrip().split('\n')
            if len(number_list) == 1:
                self.serial_no = int(number_list[0])
                return
            # end if
            number_list.sort(reverse=True)
            if self.target == 'DEVICE1' and len(number_list) > 0:
                self.serial_no = int(number_list[0])
            elif self.target == 'RECEIVER' and len(number_list) > 1:
                self.serial_no = int(number_list[1])
            elif self.target == 'DEVICE2' and len(number_list) > 2:
                self.serial_no = int(number_list[2])
            else:
                raise ValueError(f'Unknown J-Link serial number, got: {str(completed_process.stdout)}')
            # end if
        # end if
    # end def parse_args

    def run(self):  # pylint:disable=R0912
        """
        Migrates the .ini files located in the SETTINGS directory
        """
        device = self.get_device()

        if self.platform_name in self.PLATFORM_TO_UNLOCK:
            self._unlocking_device(device)
        # end if

        tmp_hex_file = None
        if self.firmware_path:
            flash_hex_file = IntelHex(self.firmware_path)
            tmp_hex_file = "temp_combi_file.hex"
            if self.nvs_path:
                nvs_hex_file = IntelHex(self.nvs_path)
                flash_hex_file.merge(nvs_hex_file, overlap='replace')
            # end if
            if self.other_file_path:
                other_hex_file = IntelHex(self.other_file_path)
                flash_hex_file.merge(other_hex_file, overlap='replace')
            # end if
            flash_hex_file.write_hex_file(tmp_hex_file, byte_count=32)
        # end if

        # Initialize an instance of a J-Link dll Library with a predefined filename
        # cf existing issue: https://github.com/square/pylink/issues/183
        dllpath = '/opt/SEGGER/JLink/libjlinkarm.so'
        lib = Library(dllpath=dllpath)
        j_link = JLink(lib)
        assert isinstance(j_link, JLink)
        assert j_link.version >= '7.88'

        try:
            # Fetch Connection Information about all USB-connected JLink emulators
            emulators: list[JLinkConnectInfo] = j_link.connected_emulators(JLinkHost.USB)
            all_emulators_str = ('All connected JLink emulators:\n' +
                                 '\n'.join(f'  [{index}] Serial Number: {emulator.SerialNumber}, '
                                           f'Product Name: {emulator.acProduct.decode()}'
                                           for index, emulator in enumerate(emulators)))

            # Verify the desired emulator is present in list of connected emulators
            if not any(e for e in emulators if e.SerialNumber == self.serial_no):
                raise JLinkException(f'The selected board serial number {self.serial_no} is not connected.\n' +
                                     all_emulators_str)
            # end if

            if self.verbose:
                self._stdout.write(f'{all_emulators_str}\n')
                self._stdout.write(f'Using board serial number {self.serial_no}\n')
            # end if

            j_link.open(self.serial_no)
            # j_link.set_tif(JLinkInterfaces.SWD)
            # TypeError: 'int' object is not callable
            # => replace the function call by the following code
            # -------- set_tif workaround ------------
            interface = JLinkInterfaces.SWD
            if not ((1 << interface) & j_link.supported_tifs()):
                raise JLinkException(f'Unsupported target interface: {interface}')
            # end if

            # The return code here is actually *NOT* the previous set interface, it
            # is ``0`` on success, otherwise ``1``.
            res = j_link._dll.JLINKARM_TIF_Select(interface)
            if res != 0:
                raise JLinkException(f'Error during SWD Interface selection: {res:d}')
            # end if
            j_link._tif = interface
            # -------- End of set_tif workaround -----

            try:
                j_link.connect(device, speed=4000)
            except JLinkException:
                if device.startswith('NRF52') or device.startswith('STM32'):
                    self._unlocking_device(device)
                # end if
                j_link.connect(device, speed=4000)
            # end try
            if self.platform_name in ['GRAVITON', 'LEXEND'] :
                j_link.reset(halt=True)
            # end if

            if self.erase_chip and self.platform_name not in self.PLATFORM_TO_UNLOCK:
                if self.verbose:
                    self._stdout.write("Erasing chip...\n")
                # end if
                try:
                    if self.platform_name == 'LEXEND':
                        # Enable external flash erasing
                        j_link.exec_command("EnableEraseAllFlashBanks")
                    # end if
                    j_link.erase()
                except JLinkEraseException as erase_exception:
                    if self.verbose:
                        self._stdout.write(f'Erase failed, retry the operation = '
                                           f'{JLinkEraseErrors.to_string(erase_exception.code)}\n')
                    # end if
                    j_link.reset(halt=True)
                    j_link.erase()
                # end try
            # end if
            if self.firmware_path:
                if self.verbose:
                    self._stdout.write("Firmware Flashing...\n")
                # end if
                try:
                    j_link.flash_file(tmp_hex_file, 0x0)
                except JLinkFlashException as flash_exception:
                    if self.verbose:
                        self._stdout.write(f'Flash failed, retry the operation = '
                                           f'{JLinkFlashException.to_string(flash_exception.code)}\n')
                    # end if
                    j_link.reset(halt=True)
                    j_link.flash_file(tmp_hex_file, 0x0)
                # end try

                if device.startswith('NRF52'):
                    self.set_application_bit(j_link)
                # end if
            # end if

            j_link.reset(halt=False)
            j_link.restart(skip_breakpoints=True)
            if self.verbose:
                self._stdout.write('Firmware successfully flashed\n')
            # end if
        except Exception as e:
            if self.verbose:
                self._stdout.write(f"Treating exception:{e}\n")
            # end if
            raise e
        finally:
            if j_link.opened():
                j_link.close()
            # end if
            remove(tmp_hex_file)
        # end try
    # end def run

    def _unlocking_device(self, device):
        """
        Trigger a full chip erase with JLinkExe
        """
        if self.verbose:
            self._stdout.write('Unlocking device, this will trigger a full chip erase...\n')
        # end if

        import pathlib
        if device.startswith('NRF52'):
            cmd = f"/opt/SEGGER/JLink/JLinkExe -device nRF52 -SelectEmuBySn {self.serial_no} -if SWD -speed 4000 " \
              f"-CommandFile {str(pathlib.Path(__file__).parent.absolute())}/recover.jlink"
        elif device.startswith('STM32'):
            cmd = f"/opt/SEGGER/JLink/JLinkExe -device {device} -SelectEmuBySn {self.serial_no} -if SWD -speed 4000 " \
                  f"-CommandFile {str(pathlib.Path(__file__).parent.absolute())}/stm_recover.jlink"
        else:
            raise ValueError("Unsupported device to unlock")
        # end if
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if self.verbose:
            if result.returncode != 0:
                output = result.stdout.decode("utf-8").split("\n")
                for line in output:
                    print("\t" + line)
                # end for
                self._stdout.write('Unlocking device FAILED\n')
            else:
                self._stdout.write('Device unlocked\n')
            # end if
        # end if

        sleep(1)
    # end def _unlocking_device

    def get_device(self):
        """
        Get device information for the given platform
        :return: device type
        :rtype: ``str``
        """
        # Target Platform selection
        # https://www.segger.com/downloads/supported-devices.php
        # Nordic Semi
        if self.platform_name == 'GRAVITON':
            device = 'NRF52840_XXAA'
        elif self.platform_name == 'QUARK':
            device = 'NRF52832_XXAA'
        elif self.platform_name == 'QUARK256':
            device = 'NRF52832_XXAB'
        elif self.platform_name == 'GLUON':
            device = 'NRF52810_XXAA'
        elif self.platform_name == 'MESON':
            device = 'NRF52820_XXAA'
        elif self.platform_name in ['HADRON', 'HADRON_GAMING']:
            device = 'NRF52833_XXAA'
        elif self.platform_name == 'STM32F0':  # STMicroelectronics
            device = 'STM32F072C8'
        elif self.platform_name == 'STM32L100':
            device = 'STM32L100C6'
        elif self.platform_name == 'STM32H7B0IB':
            device = 'STM32H7B0IB'
        elif self.platform_name == 'STM32F072CB':
            device = 'STM32F072CB'
        elif self.platform_name == 'STM32L052C8':
            device = 'STM32L052C8'
        elif self.platform_name == 'LEXEND':
            device = 'LEXEND'
        else:
            raise ValueError(f'Unknown platform, got: {self.platform_name}')
        # end if
        return device
    # end def get_device

    @staticmethod
    def set_application_bit(j_link):  # pylint:disable=R0912
        """
        Select the reboot mode of the firmware.
        Context: NRF52 Firmwares leverage the GPREGRET register to store Bootloader / Application reboot mode.

        @param: J-Link communication channel instance
        """
        gpregret_register = HexList(j_link.memory_read(GPREGRET_ADDRESS, GPREGRET_SIZE))
        if gpregret_register.testBit(BL_APP_SELECT_BIT):
            gpregret_register.clearBit(BL_APP_SELECT_BIT)
            j_link.memory_write(GPREGRET_ADDRESS, gpregret_register)

            gpregret_register_check = HexList(j_link.memory_read(GPREGRET_ADDRESS, GPREGRET_SIZE))
            assert gpregret_register_check.testBit(BL_APP_SELECT_BIT) is False
        # end if
    # end def set_application_bit
# end class Flasher


if __name__ == '__main__':
    Flasher(sys.stdout, sys.stderr)
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
