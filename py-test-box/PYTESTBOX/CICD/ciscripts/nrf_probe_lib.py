# !/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
:package: ciscripts.nrf_probe_lib
:brief: Python interface for the NORDIC nrf probe library
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/03/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import subprocess
import sys
from argparse import ArgumentParser
from os import path
from os import remove
from time import sleep

from intelhex import IntelHex
from nrf_probe_py import CoreId
from nrf_probe_py import Erase
from nrf_probe_py import ObjectData
from nrf_probe_py import Probe
from nrf_probe_py import ProbeError
from nrf_probe_py import Protection
from nrf_probe_py import Reset
from nrf_probe_py import Verify
from nrf_probe_py import version

FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("CICD")]
PYLIBRARY_DIR = path.join(WS_DIR, "LIBS", "PYLIBRARY")
if PYLIBRARY_DIR not in sys.path:
    sys.path.insert(0, PYLIBRARY_DIR)
# end if


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Flasher(object):
    """
    A program that flash a new firmware into a NRF54 platform DEV board.
    """
    VERSION = '0.1.0.0'

    # SEGGER Identifier
    SEGGER_VENDOR_ID = 0x1366

    def __init__(self, stdout, stderr):
        """
        :param  stdout: The standard output stream
        :type stdout: ``stream``
        :param  stderr: The standard error stream
        :type stderr: ``stream``
        """
        self._stdout = stdout
        self._stderr = stderr
        self.verbose = False
        self.serial_no = 0
        self._probe = None
        self.platform_name = ''
        self.firmware_app = ''
        self.firmware_rad = ''
        self._parser = None
        self.nvs_path = None
        self.erase_chip = None
        self.parse_args()
        self.result = self.run()
    # end def __init__

    def get_parser(self):
        """
        Get the ArgumentParser instance

        :return: ArgumentParser
        :rtype: ``ArgumentParser``
        """
        if self._parser is None:
            parser = ArgumentParser()
            parser.add_argument('--version', action='version', version=self.VERSION)
            parser.add_argument('-v', '--verbose', dest='verbose', help='verbose output', default=False,
                                action='store_true')
            parser.add_argument('-f', '--firmware_app', dest='firmware_app', default=None,
                                metavar='FIRMWARE', help='Firmware application file path')
            parser.add_argument('-r', '--firmware_rad', dest='firmware_rad', default=None,
                                metavar='RADIO', help='Firmware radio file path')
            parser.add_argument('-p', '--platform_name', dest='platform_name', default='TIGER',
                                metavar='PLATFORM', help='Platform DEV board name',
                                choices=[
                                    'TIGER',
                                ])
            parser.add_argument('-s', '--serial_no', dest='serial_no', default=None, metavar='SERIAL_NO',
                                type=int, help='Platform DEV board serial number')
            parser.add_argument('-n', '--nvs_path', dest='nvs_path', default=None, metavar='NVS',
                                help='Non-volatile image file path')
            parser.add_argument('-e', '--erase-chip', dest='erase_chip', default=False,
                                action='store_true', help='Perform a full chip erase')

            parser.epilog = """
Examples:
  -f //.../xxx.hex -p TIGER -s 1050871357
or
  --firmware_app build_tigermmb/zephyr/uicr_merged.hex  # .hex file path
  --firmware_rad build_tigermmb/remote/zephyr/uicr_merged.hex  # .hex file path
  --platform_name TIGER                                 # TIGER / ...
  --serial_no 1050871357                                # Unique SN of the DEV Board
  --nvs-path  /path/to/nvs.hex                          # Path of a hex file used to initialize the nvs
  --erase-chip                                          # Erase full chip, not only the pages that are written.
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
        self.firmware_app = args.firmware_app
        self.firmware_rad = args.firmware_rad
        self.platform_name = args.platform_name
        self.nvs_path = args.nvs_path
        self.serial_no = None

        if args.serial_no:
            self.serial_no = args.serial_no
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
            if len(number_list) > 0:
                self.serial_no = int(number_list[0])
            # end if
        # end if
    # end def parse_args

    def run(self):  # pylint:disable=R0912
        """
        Do the flash of selected NRF54 cpu

        :return: Flag indicating success of flashing
        :rtype: ``bool``
        """
        # Display nrf probe lib version
        self._stdout.write(f'nrf probe lib version: {version()}\n')

        tmp_app_hex_file = None
        if self.firmware_app:
            self._stdout.write(f'Application file: {self.firmware_app}\n')
            flash_hex_file = IntelHex(self.firmware_app)
            tmp_app_hex_file = "tmp_app_file.hex"
            if self.nvs_path:
                nvs_hex_file = IntelHex(self.nvs_path)
                flash_hex_file.merge(nvs_hex_file, overlap='replace')
            # end if
            flash_hex_file.write_hex_file(tmp_app_hex_file, byte_count=32)
        # end if

        tmp_rad_hex_file = None
        if self.firmware_rad:
            self._stdout.write(f'Radio core file: {self.firmware_rad}\n')
            flash_hex_file = IntelHex(self.firmware_rad)
            tmp_rad_hex_file = "tmp_rad_file.hex"
            flash_hex_file.write_hex_file(tmp_rad_hex_file, byte_count=32)
        # end if

        # Initialize an instance of a Probe
        self._probe = Probe(serial_number=int(self.serial_no), timeout_ms=2000)
        #  Get the current protection of the device.
        protection = self._probe.get_protection()
        if protection != Protection.NONE:
            self._stdout.write(f'Device protection: {self._probe.get_protection()}. Exit the flashing procedure\n')
            return False
        # end if

        if self.verbose:
            #  Retrieve the Core characteristics.
            self._stdout.write(f'Core characteristics: {self._probe.get_core_info()}\n')
        # end if

        device = self.get_device()
        #  Retrieve the MCU information.
        mcu_type = self._probe.identify()
        if isinstance(mcu_type, str):
            # old interface using string paths
            app_firmware = tmp_app_hex_file
            rad_firmware = tmp_rad_hex_file
        else:
            from nrf_probe_py import ObjectData # use a local import as only this interface has this class available
            mcu_type = mcu_type.revision_name
            app_firmware = ObjectData.from_file(tmp_app_hex_file)
            rad_firmware = ObjectData.from_file(tmp_rad_hex_file)
        # end if

        self._stdout.write(f'MCU information: {mcu_type}\n')
        if mcu_type is None or not mcu_type.startswith(device):
            # Check of MCU type failed
            self._stdout.write(f'Wrong MCU type detected: {mcu_type} while expecting {device}')
            return False
        # end if

        try:
            if self.verbose:
                self._stdout.write(f'Using board serial number {self.serial_no}\n')
            # end if

            if self.firmware_rad:
                if self.verbose:
                    self._stdout.write("Flash remote firmware\n")
                # end if
                try:
                    self._probe.erase(erase_kind=Erase.ALL, core=CoreId.NETWORK)
                except ProbeError:
                    if self.verbose:
                        self._stdout.write("Retry erasing remote firmware\n")
                    # end if
                    self._probe.erase(erase_kind=Erase.ALL, core=CoreId.NETWORK)
                # end try
                self._probe.program(firmware=rad_firmware, verify=Verify.READ, core=CoreId.NETWORK,
                                    reset_kind=None if self.firmware_app else Reset.HARD)
                sleep(.3)
            # end if

            if self.firmware_app:
                if self.verbose:
                    self._stdout.write("Flash application firmware\n")
                # end if
                self._probe.erase(erase_kind=Erase.ALL, core=CoreId.APPLICATION)
                self._probe.program(firmware=app_firmware, verify=Verify.READ, reset_kind=Reset.HARD)
                sleep(.3)
            # end if

            if self.verbose:
                self._stdout.write('Firmware successfully flashed\n')
            # end if

            return True
        except Exception as e:
            if self.verbose:
                self._stdout.write(f"Treating exception:{e}\n")
            # end if
            raise e
        finally:
            if self._probe is not None:
                self._probe.close()
            # end if
            if tmp_app_hex_file is not None:
                remove(tmp_app_hex_file)
            # end if
            if tmp_rad_hex_file is not None:
                remove(tmp_rad_hex_file)
            # end if
        # end try
    # end def run

    def get_device(self):
        """
        Get device information for the given platform
        :return: device type
        :rtype: ``str``
        """
        # Nordic Semi
        if self.platform_name == 'TIGER':
            device = 'NRF54H20_xxAA_ENGA'
        else:
            raise ValueError(f'Unknown platform, got: {self.platform_name}')
        # end if
        return device
    # end def get_device
# end class Flasher


if __name__ == '__main__':
    # flash and signal an error if the flashing fails
    if not Flasher(sys.stdout, sys.stderr).result:
        sys.exit(-1)
    # end if
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
