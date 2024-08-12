#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: ciscripts.update_hex
:brief: Script used to create a receiver firmware compatible with the APPROTECT hardware fix on NRF52 chip.
        Note that the firmware tool chain generate an .hex file with the old Build 0x0010 for the bootloader which is
        not compatible with the security update. That's why we shall leverage the IntelHex library to update the
        APPROTECT value in both the UICR and the bootloader checker function.
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/09/23
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from intelhex import IntelHex
from os.path import abspath
from os.path import join
from sys import argv
from sys import path as sys_path

# pylibrary import
FILE_PATH = abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("CICD")]
PYLIBRARY_DIR = join(WS_DIR, "LIBS", "PYLIBRARY")
if PYLIBRARY_DIR not in sys_path:
    sys_path.insert(0, PYLIBRARY_DIR)
# end if
from pylibrary.tools.elfhelper import ElfHelper  # noqa: E402: module level import not at top of file


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
# - the uicr approtect register (the prod binary is read-back protected)
UICR_APPROTECT_REGISTER_ADDRESS = 0x10001208
# - the expected_approtect value must also be different as it shall match uicr approtect value
EXPECTED_UICR_APPROTECT_VALUE_SYMBOL_NAME = 'uicr_approtectExpectedValue'
# - the value to disabled the readback protection on NRF52820 HW revision 3
APPROTECT_DISABLED = b'\x5A'


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
if __name__ == '__main__':
    if len(argv) != 3:
        exit('usage: python update_hex.py <initial_file.hex> <proj_btldr.elf>')
    # end if

    # Initialize the bootloader elf file helper
    btldr_elf_helper = ElfHelper(argv[2])

    # Extract the position of the copied Approtect byte used by the bootloader to verify the state in the UICR
    uicr_check_symbol_address = btldr_elf_helper.get_symbol_address(EXPECTED_UICR_APPROTECT_VALUE_SYMBOL_NAME)
    hex_data = IntelHex(argv[1])
    # Force the value of the copied Approtect byte
    hex_data.puts(uicr_check_symbol_address, bytes(APPROTECT_DISABLED))
    # Force the same value in the UICR register
    hex_data.puts(UICR_APPROTECT_REGISTER_ADDRESS, bytes(APPROTECT_DISABLED))
    filename, suffix = argv[1].split('.')
    approtect_filename = filename + '_approtect.' + suffix
    # Create another hex file and save the new content
    hex_data.write_hex_file(f=approtect_filename, byte_count=32)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
