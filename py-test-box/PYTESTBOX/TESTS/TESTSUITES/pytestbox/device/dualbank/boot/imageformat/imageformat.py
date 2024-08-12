#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.imageformat.imageformat
:brief: Device Dual Bank Boot Image Format tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time

from pylibrary.tools.numeral import to_int
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.dualbank.boot.imageformat.imageformattestutils import ImageFormatTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ImageFormatTestCase(DeviceBaseTestCase):
    """
    Validate Image Format
    """

    def setUp(self):
        # See ``DeviceBaseTestCase.setUp``
        self.post_requisite_reload_nvs = False
        self.post_requisite_reload_header_slot_0 = False
        self.post_requisite_reload_header_slot_1 = False
        self.post_requisite_reload_image_slot_0 = False
        self.post_requisite_reload_image_slot_1 = False
        self.post_requisite_reload_trailer_slot_0 = False
        self.post_requisite_reload_trailer_slot_1 = False

        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial slots")
        # --------------------------------------------------------------------------------------------------------------
        self.slot_0_backup = ImageFormatTestUtils.SlotFactory.create(self)
        self.slot_0_backup.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[0])
        self.slot_0_backup.init_header()

        self.slot_1_backup = ImageFormatTestUtils.SlotFactory.create(self)
        self.slot_1_backup.base_address = to_int(self.f.PRODUCT.DUAL_BANK.SLOTS.F_Base[1])
        self.slot_1_backup.init_header()

        self.slot_0_backup.init_image()
        self.slot_1_backup.init_image()

        self.slot_0_backup.init_trailer()
        self.slot_1_backup.init_trailer()
    # end def setUp

    def tearDown(self):
        # See ``CommonBaseTestCase.tearDown``
        # noinspection PyBroadException
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
            # end if
        # end with
        with self.manage_post_requisite():
            if any([self.post_requisite_reload_header_slot_0,
                    self.post_requisite_reload_image_slot_0,
                    self.post_requisite_reload_trailer_slot_0,
                    self.post_requisite_reload_header_slot_1,
                    self.post_requisite_reload_image_slot_1,
                    self.post_requisite_reload_trailer_slot_1,
                    ]):
                self.memory_manager.debugger.reset(soft_reset=False)
                self.memory_manager.debugger.stop()
                if self.post_requisite_reload_header_slot_0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Reload initial header for slot 0")
                    # --------------------------------------------------------------------------------------------------
                    self.memory_manager.debugger.writeMemory(self.slot_0_backup.base_address,
                                                             self.slot_0_backup.header_raw)
                # end if
                if self.post_requisite_reload_image_slot_0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Reload initial image for slot 0")
                    # --------------------------------------------------------------------------------------------------
                    self.memory_manager.debugger.writeMemory(
                        self.slot_0_backup.base_address + to_int(self.slot_0_backup.mcu_boot_header.ih_hdr_size),
                        self.slot_0_backup.image)
                # end if
                if self.post_requisite_reload_trailer_slot_0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Reload initial trailer for slot 0")
                    # --------------------------------------------------------------------------------------------------
                    self.memory_manager.debugger.writeMemory(self.slot_0_backup.trailer_start_address,
                                                             self.slot_0_backup.tlv_info_raw)
                    self.memory_manager.debugger.writeMemory(self.slot_0_backup.tlv_list_start_address,
                                                             self.slot_0_backup.tlv_list_raw)
                # end if
                if self.post_requisite_reload_header_slot_1:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Reload initial header for slot 1")
                    # --------------------------------------------------------------------------------------------------
                    self.memory_manager.debugger.writeMemory(self.slot_1_backup.base_address,
                                                             self.slot_1_backup.header_raw)
                # end if
                if self.post_requisite_reload_image_slot_1:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Reload initial image for slot 1")
                    # --------------------------------------------------------------------------------------------------
                    self.memory_manager.debugger.writeMemory(
                        self.slot_1_backup.base_address + to_int(self.slot_1_backup.mcu_boot_header.ih_hdr_size),
                        self.slot_1_backup.image)
                # end if
                if self.post_requisite_reload_trailer_slot_1:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(self, "Reload initial trailer for slot 1")
                    # --------------------------------------------------------------------------------------------------
                    self.memory_manager.debugger.writeMemory(self.slot_1_backup.trailer_start_address,
                                                             self.slot_1_backup.tlv_info_raw)
                    self.memory_manager.debugger.writeMemory(self.slot_1_backup.tlv_list_start_address,
                                                             self.slot_1_backup.tlv_list_raw)
                # end if
                self.memory_manager.debugger.reset(soft_reset=False)
                time.sleep(1.0)
            # end if
        # end with
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Restore debugger cache configuration')
            # ----------------------------------------------------------------------------------------------------------
            self.memory_manager.debugger.stop()
            self.memory_manager.debugger.exclude_flash_cache_range(
                self.memory_manager.debugger.NVS_START_ADDRESS,
                self.memory_manager.debugger.NVS_START_ADDRESS + self.memory_manager.debugger.NVS_SIZE)
            self.memory_manager.debugger.reset()
        # end with

        super().tearDown()
    # end def tearDown
# end class ImageFormatTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
