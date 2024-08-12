#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.memoryutils
:brief:  Helpers for manipulating data in memory
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from os import listdir
from os.path import join

# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pylibrary.tools.elfhelper import ElfHelper
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedMemoryTestUtils(CommonBaseTestUtils):
    """
    Test utils for manipulating data in memory
    """
    PATTERN = "A5"

    class StackHelper:
        """
        Stack Helper class
        """
        INITIALIZED_STACK = None

        @classmethod
        def initialize_stack_area(cls, test_case):
            """
            Initialize the full stack with a given pattern.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            if cls.INITIALIZED_STACK is None:
                stack_start_address, stack_size = cls.get_stack_address_size(test_case)

                test_case.memory_manager.debugger.writeMemory(
                    stack_start_address, HexList(SharedMemoryTestUtils.PATTERN * stack_size))
                cls.INITIALIZED_STACK = True
            # end if
        # end def initialize_stack_area

        @classmethod
        def dump_stack_area(cls, test_case):
            """
            Dump the full stack with a given pattern.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``

            :return: The stack content
            :rtype: ``HexList``
            """
            stack_start_address, stack_size = cls.get_stack_address_size(test_case)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Dump the stack area')
            # ---------------------------------------------------------------------------
            stack = test_case.memory_manager.debugger.readMemory(stack_start_address, stack_size)
            return stack
        # end def dump_stack_area

        @classmethod
        def check_stack_depth(cls, test_case, stack):
            """
            Verify that there is at least 15% of unused stack.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param stack: The stack content
            :type stack: ``HexList``

            :return: Number of unused bytes in stack
            :rtype: ``int``
            """
            byte = 0
            threshold = 12 / 100
            for byte in range(len(stack)):
                if stack[byte] != Numeral(SharedMemoryTestUtils.PATTERN):
                    test_case.assertGreater(byte, len(stack) * threshold,
                                            f"Unused stack shall be above {threshold * 100}% threshold")
                    break
                # end if
            # end for
            return byte
        # end def check_stack_depth

        @classmethod
        def get_stack_address_size(cls, test_case):
            """
            Retrieve the stack start address and size from the elf file.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``

            :return: The start address and the size of the stack
            :rtype: ``tuple[int, int]``
            """
            elf_file_path = join(TESTS_PATH, "DFU_FILES")
            app_elf_files = [file for file in listdir(elf_file_path) if file.endswith("app.elf")]
            assert len(app_elf_files) == 1, "One and only one application .elf file should be found"
            app_elf_helper = ElfHelper(join(elf_file_path, app_elf_files[0]))
            stack_start_address = app_elf_helper.get_symbol_address('__stack_start__')
            stack_size = app_elf_helper.get_symbol_address('__stack_length__')
            return stack_start_address, stack_size
        # end def get_stack_address_size

        @classmethod
        def restore_cache_settings(cls, test_case, debugger=None):
            """
            Restore the debugger cache configuration to its initial value.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param debugger: The debugger to restore
            :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger``
            """
            debugger = debugger if debugger is not None else test_case.memory_manager.debugger
            if debugger is not None:
                debugger.stop()
                debugger.exclude_flash_cache_range(
                    debugger.NVS_START_ADDRESS,
                    debugger.NVS_START_ADDRESS + debugger.NVS_SIZE)
                debugger.reset()
            # end if
        # end def restore_cache_settings
    # end class StackHelper

    class RamHelper:
        """
        RAM Helper class
        """

        @classmethod
        def _set_breakpoint(cls, test_case, symbol_names, elf_file_path):
            """
            Set a breakpoint at the address matching the given symbol

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param symbol_names: Possible names of the symbol to look for in the elf file (symbol name may vary
                                depending on the project elf file)
            :type symbol_names: ``list[str]``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: This handle to use for breakpoint operations.
            :rtype: ``int``
            """
            app_elf_helper = ElfHelper(join(TESTS_PATH, "DFU_FILES", elf_file_path))

            iter_symbol_names = iter(symbol_names)
            address = app_elf_helper.get_symbol_address(next(iter_symbol_names))
            while address is None:
                address = app_elf_helper.get_symbol_address(next(iter_symbol_names))
            # end while

            # Ensure the address is even
            address &= 0xFFFFFFFE

            breakpoint_id = test_case.memory_manager.debugger.add_breakpoint(address=address)
            return breakpoint_id
        # end def _set_breakpoint

        @classmethod
        def set_breakpoint_reset_handler(cls, test_case, elf_file_path):
            """
            Set a breakpoint at Reset_Handler address

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The handle to use for breakpoint operations.
            :rtype: ``int``
            """
            return cls._set_breakpoint(test_case=test_case,
                                       symbol_names=['Reset_Handler', 'resetHndlr'],
                                       elf_file_path=elf_file_path)
        # end def set_breakpoint_reset_handler

        @classmethod
        def set_breakpoint_main(cls, test_case, elf_file_path):
            """
            Set a breakpoint at main address

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The handle to use for breakpoint operations.
            :rtype: ``int``
            """
            return cls._set_breakpoint(test_case=test_case, symbol_names=['main'], elf_file_path=elf_file_path)
        # end def set_breakpoint_main

        @classmethod
        def dump_ram_area(cls, test_case, elf_file_path):
            """
            Dump the ram area.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The ram content
            :rtype: ``HexList``
            """
            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Dump the stack area')
            # ---------------------------------------------------------------------------
            ram_start_address, ram_size = cls.get_ram_address_size(elf_file_path)
            return test_case.memory_manager.debugger.readMemory(ram_start_address, ram_size)
        # end def dump_ram_area

        @classmethod
        def initialize_ram_area(cls, test_case, elf_file_path):
            """
            Initialize the full stack with a given pattern.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``
            """
            ram_start_address, ram_size = cls.get_ram_address_size(elf_file_path)

            test_case.memory_manager.debugger.writeMemory(
                ram_start_address, HexList(SharedMemoryTestUtils.PATTERN * ram_size))
        # end def initialize_stack_area

        @classmethod
        def get_ram_address_size(cls, elf_file_path):
            """
            Retrieve the RAM start address and size from the elf file.

            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The start address and the size of the RAM
            :rtype: ``tuple[int, int]``
            """
            app_elf_helper = ElfHelper(join(TESTS_PATH, "DFU_FILES", elf_file_path))
            ram_start_address = app_elf_helper.get_symbol_address('__data_start__')
            ram_size = app_elf_helper.get_symbol_address('__data_length__')
            return ram_start_address, ram_size
        # end def get_ram_address_size

        @classmethod
        def get_ram_noinit_address_size(cls, elf_file_path):
            """
            Retrieve the RAM no init start address and size from the elf file.

            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The start address and the size of the RAM no init
            :rtype: ``tuple[int, int]``
            """
            app_elf_helper = ElfHelper(join(TESTS_PATH, "DFU_FILES", elf_file_path))
            start_address = app_elf_helper.get_symbol_address('__noinit_start__')
            size = app_elf_helper.get_symbol_address('__noinit_length__')
            return start_address, size
        # end def get_ram_noinit_address_size

        @classmethod
        def dump_copy_flash_area(cls, test_case, elf_file_path):
            """
            Dump the copy of the ram initialization data in flash.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The ram content
            :rtype: ``HexList``
            """
            copy_flash_start_address, copy_flash_size = cls.get_copy_flash_address_size(elf_file_path)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, 'Exclude the FLASH from debugger cache, to force new memory read from device each time')
            # ---------------------------------------------------------------------------
            test_case.memory_manager.debugger.exclude_flash_cache_range(copy_flash_start_address, copy_flash_start_address +
                                                                        copy_flash_size)

            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Dump the flash area used to initialize the RAM')
            # ---------------------------------------------------------------------------
            ram = test_case.memory_manager.debugger.readMemory(copy_flash_start_address, copy_flash_size)
            return ram
        # end def dump_copy_flash_area

        @classmethod
        def get_copy_flash_address_size(cls, elf_file_path):
            """
            Retrieve the FLASH area used to initialize the RAM. Get the start address and size from elf file.

            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The start address and the size of the FLASH to copy
            :rtype: ``tuple[int, int]``
            """
            app_elf_helper = ElfHelper(join(TESTS_PATH, "DFU_FILES", elf_file_path))
            copy_flash_start_address = app_elf_helper.get_symbol_address('__etext')
            copy_flash_size = app_elf_helper.get_symbol_address('__data_length__')
            return copy_flash_start_address, copy_flash_size
        # end def get_copy_flash_address_size

        @classmethod
        def dump_bss_area(cls, test_case, elf_file_path):
            """
            Dump the bss area

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The bss content
            :rtype: ``HexList``
            """
            # ---------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Dump the bss area')
            # ---------------------------------------------------------------------------
            bss_start_address, bss_size = cls.get_bss_address_size(elf_file_path)
            return test_case.memory_manager.debugger.readMemory(bss_start_address, bss_size)
        # end def dump_ram_area

        @classmethod
        def initialize_bss_area(cls, test_case, elf_file_path):
            """
            Initialize the bss with a given pattern.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``
            """
            bss_start_address, bss_size = cls.get_bss_address_size(elf_file_path)

            test_case.memory_manager.debugger.writeMemory(
                bss_start_address, HexList(SharedMemoryTestUtils.PATTERN * bss_size))
        # end def initialize_stack_area

        @classmethod
        def get_bss_address_size(cls, elf_file_path):
            """
            Retrieve the bss start address and size from the elf file.

            :param elf_file_path: The path to the targeted .elf file
            :type elf_file_path: ``str``

            :return: The start address and the size of the bss
            :rtype: ``tuple[int, int]``
            """
            app_elf_helper = ElfHelper(join(TESTS_PATH, "DFU_FILES", elf_file_path))
            bss_start_address = app_elf_helper.get_symbol_address('__bss_start__')
            bss_size = app_elf_helper.get_symbol_address('__bss_length__')
            return bss_start_address, bss_size
        # end def get_bss_address_size
# end class SharedMemoryTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
