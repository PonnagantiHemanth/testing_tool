#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: ciscripts.compare_hex
:brief: Binary files comparison script
:author: Nestor Lopez Casado/Christophe Roquebert <nlopezcasad@logitech.com>/<croquebert@logitech.com>
:date: 2020/03/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from argparse import ArgumentParser
from argparse import RawTextHelpFormatter
from os import path
from sys import path as sys_path
from sys import stdout

from Crypto.PublicKey import RSA
from intelhex import IntelHex
from intelhex import NotEnoughDataError

# Get PYLIBRARY
FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("CICD")]
PYLIBRARY_DIR = path.join(WS_DIR, "LIBS", "PYLIBRARY")
if PYLIBRARY_DIR not in sys_path:
    sys_path.insert(0, PYLIBRARY_DIR)
# end if
from pylibrary.tools.elfhelper import ElfHelper  # noqa: E402: module level import not at top of file


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
# for nrf52 platform, the differences allowed between the production binary
# and the ci binary are listed below.
# - the uicr approtect register (the prod binary is read-back protected)
uicr_approtect_register_address = 0x10001208
# - the expected_approtect value must also be different as it shall match uicr approtect value
expected_uicr_approtect_value_symbol_name = 'uicr_approtectExpectedValue'
# - the value to enable the readback protection on NRF52
APPROTECT_ENABLED = b'\x00'
# - the public encryption keys are different
public_key_symbol_name = 'rsa_keyMod'
# - the build type (dirty bit, ci_build_bit) are also different.
fw_data_symbol_name = 'fwd_currentFwData'
default_flash_settings = "defaultFlashSettings"
# - the offset of build_info byte within the fwd_data structure.
build_info_byte_offset = 19
# x1602 pass-word authentication feature parameters:
# - the manufacturing password salt
expected_x1602_manuf_salt_symbol_name = 'x1602_tstManuf_salt'
# - the manufacturing password digest
expected_x1602_manuf_dgst_symbol_name = 'x1602_tstManuf_dgst'
# - the manufacturing password salt
expected_x1602_compl_salt_symbol_name = 'x1602_tstCompl_salt'
# - the manufacturing password digest
expected_x1602_tstCompl_dgst_symbol_name = 'x1602_tstCompl_dgst'
# - the ble advertising undirected timeout
undirected_timeout_symbol_name = 'lble_gap_advertisingTimeout10msec'
# - the ble advertising directed (reconnection) timeout
directed_timeout_symbol_name = 'lble_gap_reconnectionTimeout10msec'
# - gaming LS2 disconnection timeout (duration between sleep to deep sleep)
eqcomm_disconnect_timeout_symbol_name = 'eqcomm_disconnectTimeout1sec'
# - gaming BLE gap disconnection time (duration between sleep to deep sleep)
lblecomm_disconnect_timeout_symbol_name = 'lblecomm_disconnectTimeout1sec'

# bootloader addresses symbol names
bootloader_start_symbol_name = '__Vectors'
bootloader_end_symbol_name = 'nvs_init'

# Spurious motion timeout set in sensor register
spurious_motion_register_settings_symbol_name = 'em7792_initRegSettings'
# - the offset of REG_RestToSTime register value within the em7792_initRegSettings structure.
spurious_motion_register_settings_offset = 15
# Spurious motion timeout used in algorithm
spurious_motion_timeout_symbol_name = 'sensorRest3EntryTime'

# Add verbosity to the process
VERBOSE = False


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class Options:
    """
    Define the list of valid script options
    """
    # Option to enable the verification between Production and Test (CPPFLAGS=-DCI_BUILD=1) firmwares
    BUILD_CI_CHECK = 'build_ci_check'
    # Option to enable the verification of the bootloader integrity
    BOOTLOADER_CHECK = 'bootloader_check'

    VALID_LIST = [BUILD_CI_CHECK, BOOTLOADER_CHECK]
# end class Options


class HexCompare:
    """
    Binary files comparison class
    """

    def __init__(self):
        self.file_to_validate = None
        self.reference_hex = None
        self.reference_data = None
        self.reference_addresses = None
        self.btldr_elf_helper = None
        self.app_elf_helper = None
        self.options = None
        self.is_gaming_product = False
        self.rsa_key_path = None

        self._parser = None
        self.parse_args()

        assert self.file_to_validate is not None
        assert self.reference_hex is not None
        assert self.btldr_elf_helper is not None

        if self.options == Options.BUILD_CI_CHECK:
            # Verify the second binary is a production firmware
            self.check_approtect_enabled(production_firmware=self.file_to_validate, elf_helper=self.btldr_elf_helper)
            # list of variables stored in flash whose value can differ between the two
            # input hex files, these are the expected value of approtect and the public
            # key used to validate the signature of the dfu.
            # list of specific addresses that can differ, this is the address of uicr approtect register
            if VERBOSE:
                stdout.write("First allowed address is the one for the uicr approtect register: "
                             f"0x{uicr_approtect_register_address:X}\n")
            # end if
            addresses_allowed_to_differ = {uicr_approtect_register_address}

            if VERBOSE:
                stdout.write("Look at the allowed symbols in the bootloader elf file:\n")
            # end if
            if self.btldr_elf_helper is not None:
                symbols = [public_key_symbol_name, expected_uicr_approtect_value_symbol_name,
                           undirected_timeout_symbol_name, directed_timeout_symbol_name]
                for name in symbols:
                    addresses_allowed_to_differ = self.add_address_to_allowed_difference(
                        allowed_set=addresses_allowed_to_differ, elf_helper=self.btldr_elf_helper, symbol_name=name,
                        entity_in_log="\tBootloader")
                # end for

                addresses_allowed_to_differ = self.add_address_to_allowed_difference(
                    allowed_set=addresses_allowed_to_differ, elf_helper=self.btldr_elf_helper,
                    symbol_name=fw_data_symbol_name,
                    entity_in_log="\tBootloader", one_byte_offset=build_info_byte_offset)
            # end if

            if VERBOSE:
                stdout.write("Look at the allowed symbols in the application elf file:\n")
            # end if
            if self.app_elf_helper is not None:
                symbols = [expected_uicr_approtect_value_symbol_name, expected_x1602_manuf_salt_symbol_name,
                           expected_x1602_manuf_dgst_symbol_name, expected_x1602_compl_salt_symbol_name,
                           expected_x1602_tstCompl_dgst_symbol_name, default_flash_settings,
                           spurious_motion_timeout_symbol_name]
                if self.is_gaming_product:
                    symbols += [eqcomm_disconnect_timeout_symbol_name, lblecomm_disconnect_timeout_symbol_name]
                # end if
                for name in symbols:
                    addresses_allowed_to_differ = self.add_address_to_allowed_difference(
                        allowed_set=addresses_allowed_to_differ, elf_helper=self.app_elf_helper, symbol_name=name,
                        entity_in_log="\tApplication")
                # end for
                addresses_allowed_to_differ = self.add_address_to_allowed_difference(
                    allowed_set=addresses_allowed_to_differ, elf_helper=self.app_elf_helper,
                    symbol_name=fw_data_symbol_name,
                    entity_in_log="\tApplication", one_byte_offset=build_info_byte_offset)
                addresses_allowed_to_differ = self.add_address_to_allowed_difference(
                    allowed_set=addresses_allowed_to_differ, elf_helper=self.app_elf_helper,
                    symbol_name=spurious_motion_register_settings_symbol_name,
                    entity_in_log="\tApplication", one_byte_offset=spurious_motion_register_settings_offset)
            # end if

            if not self.is_same_hex(hex_file=self.file_to_validate, ignored_addresses=addresses_allowed_to_differ):
                exit(2)
            # end if

            # Verify the RSA public key stored in the bootloader matches the expected NPI key saved in pem file
            if self.rsa_key_path is not None:
                # Load RSA private key
                rsa_key = RSA.import_key(open(self.rsa_key_path).read())
                bytes_val = rsa_key.n.to_bytes(rsa_key.size_in_bytes(), 'little')
                symbol_address = self.btldr_elf_helper.get_symbol_address(name=public_key_symbol_name)
                prod_hex_file = IntelHex(self.file_to_validate)
                prod_rsa_key_value = prod_hex_file.tobinstr(
                    start=symbol_address, end=symbol_address + rsa_key.size_in_bytes() - 1)

                if not bytes_val == prod_rsa_key_value:
                    stdout.write(f"RSA public key does not match the expected value (Got {prod_rsa_key_value.hex()}"
                                 f"while expecting {bytes_val.hex()})\n")
                    exit(2)
                else:
                    stdout.write("RSA public key verified")
                # end if
            # end if
        else:
            bootloader_start_address = self.btldr_elf_helper.get_symbol_address(bootloader_start_symbol_name)
            bootloader_end_address = self.btldr_elf_helper.get_symbol_address(bootloader_end_symbol_name) - 1
            if not self.is_same_bootloader(hex_file=self.file_to_validate, start_address=bootloader_start_address,
                                           end_address=bootloader_end_address):
                stdout.write("Different bootloader data\n")
                exit(2)
            # end if
            stdout.write("Same bootloader data\n")
        # end if
    # end def __init__

    def get_parser(self):
        """
        Get the ArgumentParser instance

        :return: ArgumentParser instance
        :rtype: ``ArgumentParser``
        """
        if self._parser is None:
            parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
            parser.add_argument('-f', '--firmware_path', dest='firmware_path', metavar='FIRMWARE',
                                help='Firmware file path')
            parser.add_argument('-c', '--ci_build_path', dest='ci_build_path', metavar='CI_BUILD',
                                help='CI build file path')
            parser.add_argument('-b', '--ci_bootloader_path', dest='ci_bootloader_path', metavar='CI_BOOTLOADER',
                                help='CI bootloader file path')
            parser.add_argument('-e', '--ci_app_path', dest='ci_app_path', metavar='CI_APP', help='CI app file path')
            parser.add_argument('-a', '--action', dest='action', default='build_ci_check', metavar='ACTION',
                                help='[OPTIONAL] Possible actions: build_ci_check or bootloader_check. '
                                     'Default value: build_ci_check')
            parser.add_argument('-g', '--gaming_product', dest='is_gaming_product', default=False,
                                metavar='IS_GAMING_PRODUCT',
                                help="[OPTIONAL] The flag indicating if it's a gaming products. Default value: False")
            parser.add_argument('-r', '--rsa_key_path', dest='rsa_key_path', metavar='RSA_KEY',
                                help='RSA key file path')
            parser.epilog = """
    Examples:
    PWS Product:
      -f firmware_file.hex -c ci_build_file.hex -b ci_btldr_file.elf -e ci_app_file.elf -a build_ci_check
    GAMING Product: (Set -g True if the deep sleep duration be shorten to LS2: 2 minutes, BLE: 4 minutes)
      -f firmware_file.hex -c ci_build_file.hex -b ci_btldr_file.elf -e ci_app_file.elf -a bootloader_check -g True
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
        self.file_to_validate = args.firmware_path
        self.reference_hex = args.ci_build_path
        self.reference_data = IntelHex(self.reference_hex).todict()
        self.reference_addresses = self.reference_data.keys()
        self.btldr_elf_helper = ElfHelper(args.ci_bootloader_path) if args.ci_bootloader_path is not None else None
        self.app_elf_helper = ElfHelper(args.ci_app_path) if args.ci_app_path is not None else None
        assert args.action in Options.VALID_LIST
        self.options = Options.BOOTLOADER_CHECK if args.action == 'bootloader_check' else Options.BUILD_CI_CHECK
        self.is_gaming_product = args.is_gaming_product
        self.rsa_key_path = args.rsa_key_path
    # end def parse_args

    def is_same_hex(self, hex_file, ignored_addresses=None):
        """
        Compare the given binary file with self excluding some address ranges

        :param hex_file: given binary file
        :type hex_file: ``str``
        :param ignored_addresses: List of address range to ignore - OPTIONAL
        :type ignored_addresses: ``set`` or ``None``

        :return: Report whether all the differences are contained in the ignored addresses set.
        :rtype: ``bool``
        """
        if VERBOSE:
            stdout.write("Check if the hex files are identical (or with some allowed difference):\n\t")
        # end if
        ignored_address_set = set() if ignored_addresses is None else ignored_addresses

        hex_data = IntelHex(hex_file).todict()
        hex_addresses = hex_data.keys()
        # ensure that the hex data provided by the two files covers the same addresses.
        if hex_addresses != self.reference_addresses:
            if VERBOSE:
                stdout.write(f"Different address ranges detected: {len(hex_addresses)} ! = "
                             f"{len(self.reference_addresses)}")
            # end if
            return False
        # end if

        addresses_with_different_contents = set(x for x in hex_data if hex_data[x] != self.reference_data[x])

        # ensure that the data that differs between the two hex files is found at a
        # subset of the addresses of the symbols that are allowed to change between
        # production and ci hex files.
        if not addresses_with_different_contents.issubset(ignored_address_set):
            if VERBOSE:
                difference = [f"{x:X}" for x in addresses_with_different_contents.difference(ignored_address_set)]
                stdout.write(f"Different addresses: {difference}\n\t")
            # end if
            stdout.write("Different hex file\n")
            return False
        # end if

        stdout.write("Same hex file\n")
        return True
    # end def is_same_hex

    def is_same_bootloader(self, hex_file, start_address, end_address):
        """
        Compare the bootloader addresses set of the given binary file with self

        :param hex_file: given binary file
        :type hex_file: ``str``
        :param start_address: Bootloader start address
        :type start_address: ``int``
        :param end_address: Bootloader end address
        :type end_address: ``int``

        :return: Report whether both bootloader addresses set match.
        :rtype: ``bool``
        """
        hex_data = IntelHex(hex_file).todict()

        for x in range(start_address, end_address):
            if x not in hex_data.keys():
                if x in self.reference_data.keys():
                    # Bootloader reference file is larger than the new one
                    return False
                else:
                    # Address is neither in the reference set, nor in the new build
                    continue
                # end if
            elif x not in self.reference_data.keys() and x in hex_data.keys():
                # New bootloader file is larger than the reference
                return False
            elif hex_data[x] != self.reference_data[x]:
                # Data are different
                return False
            # end if
        # end for
        return True
    # end def is_same_bootloader

    @classmethod
    def get_symbol_address_range(cls, elf_helper, symbol_name):
        """
        Get a symbol address range in an efl file. If the symbol is not present in the elf file, ``None`` is returned.

        If the symbol is in RAM, the address range returned will be from the preloading space addresses and not the
        address in RAM.

        :param elf_helper: Elf helper object containing the information
        :type elf_helper: ``ElfHelper``
        :param symbol_name: Name of the symbol to find
        :type symbol_name: ``str``

        :return: The address range (if possible)
        :rtype: ``set`` or ``None``

        :raise ``AssertionError``: __etext, __data_start__ or __data_end__ symbols are not in the elf file
        """
        symbol_address = elf_helper.get_symbol_address(name=symbol_name)
        if symbol_address is None:
            return None
        # end if

        # Sanity check
        etext_addr = elf_helper.get_symbol_address(name="__etext")
        data_start_addr = elf_helper.get_symbol_address(name="__data_start__")
        data_end_addr = elf_helper.get_symbol_address(name="__data_end__")

        etext_addr = etext_addr if etext_addr is not None else elf_helper.get_symbol_address(name="_etext")
        data_start_addr = data_start_addr if data_start_addr is not None else elf_helper.get_symbol_address(
            name="_sdata")
        data_end_addr = data_end_addr if data_end_addr is not None else elf_helper.get_symbol_address(name="_sdata")

        assert etext_addr is not None, "End of text symbol should be in the elf file"
        assert data_start_addr is not None, "Data start symbol should be in the elf file"
        assert data_end_addr is not None, "Data end symbol should be in the elf file"

        symbol_address_range = elf_helper.get_symbols_address_range(symbols_names=[symbol_name])
        symbol_address_range = list(symbol_address_range)
        symbol_address_range.sort()
        symbol_address_range = set(symbol_address_range)

        if data_start_addr <= symbol_address <= data_end_addr:
            address_delta = data_start_addr - etext_addr
            symbol_address_range = set([x - address_delta for x in list(symbol_address_range)])
        # end if

        return symbol_address_range
    # end def get_symbol_address_range

    @classmethod
    def add_address_to_allowed_difference(cls, allowed_set, elf_helper, symbol_name, entity_in_log=None,
                                          one_byte_offset=None):
        """
        Add all addresses associated to a symbol to a set of addresses that are allowed to have a different value
        in memory.
        If the symbol is not in the elf file, nothing is done.
        If ``one_byte_offset`` is not ``None``, only the address at the index in the range will be taken.

        :param allowed_set: Set of allowed addresses to add the new ones (if found)
        :type allowed_set: ``set``
        :param elf_helper: Elf helper object containing the information
        :type elf_helper: ``ElfHelper``
        :param symbol_name: Name of the symbol to find
        :type symbol_name: ``str``
        :param entity_in_log: Entity to print in log - OPTIONAL
        :type entity_in_log: ``str`` or ``None``
        :param one_byte_offset: Offset of the only byte accepted after the first address - OPTIONAL
        :type one_byte_offset: ``int`` or ``None``

        :return: The new set with added values (if needed)
        :rtype: ``set``
        """
        log_to_add = entity_in_log + " s" if entity_in_log is not None else "S"

        if one_byte_offset is None:
            symbol_address_range = cls.get_symbol_address_range(elf_helper=elf_helper, symbol_name=symbol_name)
        else:
            symbol_address = elf_helper.get_symbol_address(name=symbol_name)
            if symbol_address is None:
                symbol_address_range = None
            else:
                symbol_address_range = {symbol_address + one_byte_offset}
            # end if
        # end if

        if symbol_address_range is None:
            if VERBOSE:
                stdout.write(f"{log_to_add}ymbol not found: {symbol_name}\n")
            # end if
            return allowed_set
        # end if

        allowed_set |= symbol_address_range
        if VERBOSE:
            if len(symbol_address_range) > 1:
                stdout.write(
                    f"{log_to_add}ymbol found: {symbol_name} at address range [0x{list(symbol_address_range)[0]:X}, "
                    f"0x{list(symbol_address_range)[-1]:X}]\n")
            else:
                stdout.write(
                    f"{log_to_add}ymbol found: {symbol_name} at address 0x{list(symbol_address_range)[0]:X}\n")
            # end if
        # end if

        return allowed_set
    # end def add_address_to_allowed_changes

    @classmethod
    def check_approtect_enabled(cls, production_firmware, elf_helper):
        """
        Verify the Access port protection register in UICR set to Enabled

        :param production_firmware: the binary file compiled with BUILD_CONFIG=PROD
        :type production_firmware: ``str``
        :param elf_helper: helper objet handling bootloader elf file
        :type elf_helper: ``ElfHelper``
        """
        hex_data = IntelHex(production_firmware)
        # Verify the same value in the UICR register
        # https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.nrf52832.ps.v1.1%2Fuicr.html&cp=4_2_0_13_0_61&anchor=register.APPROTECT
        try:
            assert hex_data.gets(uicr_approtect_register_address, 1) == bytes(APPROTECT_ENABLED), \
                "UICR APPROTECT register is not enabled "
        except NotEnoughDataError as err:
            stdout.write(f"No Access port protection found: {err}\n")
            return
        # end try
        if elf_helper is not None:
            # Extract the position of the copied Approtect byte used by the bootloader to verify the state in the UICR
            uicr_check_symbol_address = elf_helper.get_symbol_address(expected_uicr_approtect_value_symbol_name)
            # Verify the value of the copied Approtect byte
            assert hex_data.gets(uicr_check_symbol_address, 1) == bytes(APPROTECT_ENABLED), \
                "Bootloader check value does not match the enabled constant"
        # end if
    # end def check_approtect_enabled
# end HexCompare


if __name__ == '__main__':
    HexCompare()
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
