#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
@package pylibrary.tools.elfhelper

@brief elf files handling classes

@author nestor lopez casado

@date   2019/11/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class ElfHelper:
    def __init__(self, elf_file):
        self.elf_file = elf_file

    # returns a set with all the addresses spanning across each symbol memory range,
    # these addresses can be used as an input to the is_same_hex() method.
    def get_symbols_address_range(self, symbols_names=None):
        symbols_addresses = set()
        if symbols_names is None:
            return symbols_addresses

        with open(self.elf_file, 'rb') as f:
            elf_object = ELFFile(f)
            symbol_table = elf_object.get_section_by_name('.symtab')
            assert (isinstance(symbol_table, SymbolTableSection))
            symbols_allowed_to_differ = []
            for name in symbols_names:
                if symbol_table.get_symbol_by_name(name) is not None:
                    symbols_allowed_to_differ.append(symbol_table.get_symbol_by_name(name)[0])
                # end if
            # end for

            for i in symbols_allowed_to_differ:
                symbols_addresses |= set(x for x in range(i['st_value'], i['st_value'] + i['st_size']))
            # end for

            return symbols_addresses
        # end with

    # end get_symbols_address_range

    # this returns the start address of a symbol.
    def get_symbol_address(self, name):
        with open(self.elf_file, 'rb') as f:
            elf_object = ELFFile(f)
            symbol_table = elf_object.get_section_by_name('.symtab')
            assert (isinstance(symbol_table, SymbolTableSection))
            if symbol_table.get_symbol_by_name(name) is not None:
                return symbol_table.get_symbol_by_name(name)[0]['st_value']
            else:
                return None
            # end if
        # end with
    # end get_symbol_address
# end ElfHelper

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------