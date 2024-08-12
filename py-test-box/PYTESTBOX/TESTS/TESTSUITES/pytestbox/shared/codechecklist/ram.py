#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.shared.codechecklist.ram
:brief: Shared Ram tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/07/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from os import listdir
from os.path import join
from time import sleep

from pychannel.blechannel import BleChannel
from pychannel.usbchannel import UsbChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.memoryutils import SharedMemoryTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedRamTestCase(CommonBaseTestCase, ABC):
    """
    Validate Ram initialization
    """
    def setUp(self):
        # See ``CommonBaseTestCase.setUp``

        # Start with super setUp()
        super().setUp()

        # Stop Task executor
        ChannelUtils.close_channel(test_case=self)

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Clear all breakpoints")
        # ------------------------------------------------------------------------
        if self.memory_manager.debugger is not None:
            self.memory_manager.debugger.clear_breakpoints()
        # end if
    # end def setUp

    def tearDown(self):
        # See ``CommonBaseTestCase.tearDown``
        with self.manage_post_requisite():
            # ------------------------------------------------------------------------
            LogHelper.log_post_requisite(test_case=self, text="Clear all breakpoints and re-run the code")
            # ------------------------------------------------------------------------
            if self.memory_manager.debugger is not None:
                self.memory_manager.debugger.clear_breakpoints()
                self.memory_manager.debugger.run(skip_current_breakpoint=True)
            # end if
            sleep(1)
        # end with

        with self.manage_post_requisite():
            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(test_case=self, text="Restore debugger cache settings")
            # ------------------------------------------------------------------------------------------------------
            SharedMemoryTestUtils.StackHelper.restore_cache_settings(test_case=self)

            if isinstance(self.current_channel, (UsbChannel, BleChannel)):
                ChannelUtils.wait_usb_ble_channel_connection_state(
                    test_case=self,
                    channel=self.current_channel,
                    connection_state=True)
            # end if
            # Start Task executor
            ChannelUtils.open_channel(test_case=self)
        # end with
        super().tearDown()
    # end def tearDown

    def _verify_ram_bss_initialization(self, elf_file_path):
        """
        Verify RAM area for variables that shall be at 0 (i.e. bss) or non 0 (i.e. ram) at init

        :param elf_file_path: The path to the targeted .elf file
        :type elf_file_path: ``str``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump __etext area content which is used to initialize the ram')
        # --------------------------------------------------------------------------------------------------------------
        copy_flash = SharedMemoryTestUtils.RamHelper.dump_copy_flash_area(test_case=self, elf_file_path=elf_file_path)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set an hardware breakpoint at the start of the Reset handler routine')
        # --------------------------------------------------------------------------------------------------------------
        SharedMemoryTestUtils.RamHelper.set_breakpoint_reset_handler(test_case=self, elf_file_path=elf_file_path)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Reset the DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.reset(soft_reset=True)
        sleep(1.0)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify we hit the breakpoint in the reset handler routine')
        # --------------------------------------------------------------------------------------------------------------
        self.assertFalse(self.memory_manager.debugger.isRunning(), "Firmware doesn't stop on reset handler breakpoint")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set an hardware breakpoint at the start of the main routine')
        # --------------------------------------------------------------------------------------------------------------
        SharedMemoryTestUtils.RamHelper.set_breakpoint_main(test_case=self, elf_file_path=elf_file_path)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Overwrite the full ram area with a known pattern')
        # --------------------------------------------------------------------------------------------------------------
        SharedMemoryTestUtils.RamHelper.initialize_ram_area(test_case=self, elf_file_path=elf_file_path)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Overwrite the bss area with a known pattern')
        # --------------------------------------------------------------------------------------------------------------
        SharedMemoryTestUtils.RamHelper.initialize_bss_area(test_case=self, elf_file_path=elf_file_path)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Execute instructions until the second breakpoint')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.debugger.run(skip_current_breakpoint=True)
        sleep(.1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify we hit the breakpoint in the main routine')
        # --------------------------------------------------------------------------------------------------------------
        self.assertFalse(self.memory_manager.debugger.isRunning(), "Firmware doesn't stop on main breakpoint")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the ram content when firmware is halted at the start of the main routine')
        # --------------------------------------------------------------------------------------------------------------
        ram_after_main_crt_startup = SharedMemoryTestUtils.RamHelper.dump_ram_area(
            test_case=self, elf_file_path=elf_file_path)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check RAM content after initialization matches its copy in Flash')
        # ---------------------------------------------------------------------------
        self.assertEqual(copy_flash,
                         ram_after_main_crt_startup,
                         "After initialization, RAM shall matche its copy in Flash")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Dump the bss content when firmware is halted at the start of the main routine')
        # --------------------------------------------------------------------------------------------------------------
        bss_after_main_crt_startup = SharedMemoryTestUtils.RamHelper.dump_bss_area(
            test_case=self, elf_file_path=elf_file_path)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check RAM content after initialization matches its copy in Flash')
        # ---------------------------------------------------------------------------
        self.assertEqual(HexList("00" * len(bss_after_main_crt_startup)),
                         bss_after_main_crt_startup,
                         "After initialization, RAM shall matche its copy in Flash")
    # end def _verify_ram_bss_initialization

    @features('RamInit')
    @level('Functionality')
    @services('Debugger')
    def test_bootloader_ram_initialization(self):
        """
        Verify RAM area for variables that shall be at 0 (i.e. bss) or non 0 (i.e. ram) at init during bootloader
        execution
        """
        if self.f.PRODUCT.CODE_CHECKLIST.F_BootLoaderElfFileName is None:
            elf_file_path = f'{self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName[:-8]}btldr.elf'
        else:
            elf_file_path = f'{self.f.PRODUCT.CODE_CHECKLIST.F_BootLoaderElfFileName}'
        # end if

        self._verify_ram_bss_initialization(elf_file_path=elf_file_path)

        self.testCaseChecked("FUN_RAM_0001")
    # end def test_bootloader_ram_initialization

    @features('RamInit')
    @level('Functionality')
    @services('Debugger')
    def test_application_ram_initialization(self):
        """
        Verify RAM area for variables that shall be at 0 (i.e. bss) or non 0 (i.e. ram) at init during application
        execution
        """
        elf_file_path = join(TESTS_PATH, "DFU_FILES")
        app_elf_files = [file for file in listdir(elf_file_path) if file.endswith("app.elf")]
        assert len(app_elf_files) == 1, "One and only one application .elf file should be found"
        elf_file_path = join(elf_file_path, app_elf_files[0])

        self._verify_ram_bss_initialization(elf_file_path=elf_file_path)

        self.testCaseChecked("FUN_RAM_0002")
    # end def test_application_ram_initialization

# end class SharedRamTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
