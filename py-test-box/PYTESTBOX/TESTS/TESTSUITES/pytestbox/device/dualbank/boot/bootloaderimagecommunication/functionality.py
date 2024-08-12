#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.dualbank.boot.bootloaderimagecommunication.functionality
:brief: Device Dual Bank Boot Bootloader Image Communication Functionality tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import time

from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.mcu.mcuboot.imageformat import BootImageCommunication
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.bootloaderimagecommunication import \
    BootloaderImageCommunicationTestCase
from pytestbox.device.dualbank.boot.bootloaderimagecommunication.bootloaderimagecommunicationtestutils import \
    BootloaderImageCommunicationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BootloaderImageCommunicationFunctionalityTestCase(BootloaderImageCommunicationTestCase):
    """
    Validate Bootloader to Image Communication Functionality Case
    """

    @features('DualBank')
    @level('Functionality')
    def test_warm_boot(self):
        """
        Check current boot type flag is cleared (0) when the current boot is a warm boot
        """
        self._test_boot_type(BootImageCommunication.BlToImgFlags.BootType.WARM_BOOT)
        self.testCaseChecked("FUN_DUAL_BANK_COM_0001")
    # end def test_warm_boot

    @features('DualBank')
    @level('Functionality')
    def test_cold_boot(self):
        """
        Check current boot type flag is set (1) when the current boot is a cold boot
        """
        self._test_boot_type(BootImageCommunication.BlToImgFlags.BootType.COLD_BOOT)
        self.testCaseChecked("FUN_DUAL_BANK_COM_0002")
    # end def test_cold_boot

    def _test_boot_type(self, boot_type):
        """
        Check current boot type flag status for a given boot type

        :param boot_type: Boot type
        :type boot_type: ``BootImageCommunication.BlToImgFlags.BootType``
        """
        if boot_type == BootImageCommunication.BlToImgFlags.BootType.WARM_BOOT:
            soft_reset = True
            reset_name = "soft"
        elif boot_type == BootImageCommunication.BlToImgFlags.BootType.COLD_BOOT:
            soft_reset = False
            reset_name = "hard"
        else:
            raise KeyError("Unknown boot type")
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Reset device ({reset_name} reset)")
        # --------------------------------------------------------------------------------------------------------------
        self.device_debugger.reset(soft_reset=soft_reset)
        time.sleep(self.config_manager.get_feature(self.config_manager.ID.STARTUP_TIME_COLD_BOOT) / 1000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get bootloader image communication bootloader to image flags")
        # --------------------------------------------------------------------------------------------------------------
        bl_to_img_flags = BootloaderImageCommunicationTestUtils.get_bl_to_img_flags(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self,
                            "Check current boot type flag in bootloader image communication bootloader to image flags")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=boot_type,
                         obtained=bl_to_img_flags.boot_type,
                         msg="Current boot type flag doesn't match")
    # end def _test_boot_type

    @features('DualBank')
    @level('Functionality')
    def test_cold_boot_request(self):
        """
        Check cold boot request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set cold boot request flag")
        # --------------------------------------------------------------------------------------------------------------
        BootloaderImageCommunicationTestUtils.set_cold_boot_request(test_case=self, cold_boot_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Reset device (soft reset)")
        # --------------------------------------------------------------------------------------------------------------
        self.device_debugger.reset(soft_reset=True)
        time.sleep(self.config_manager.get_feature(self.config_manager.ID.STARTUP_TIME_COLD_BOOT) / 1000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get bootloader image communication bootloader to image flags")
        # --------------------------------------------------------------------------------------------------------------
        bl_to_img_flags = BootloaderImageCommunicationTestUtils.get_bl_to_img_flags(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check current boot type flag")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=BootImageCommunication.BlToImgFlags.BootType.COLD_BOOT,
                         obtained=bl_to_img_flags.boot_type,
                         msg="Current boot type should be cold boot")

        self.testCaseChecked("FUN_DUAL_BANK_COM_0003")
    # end def test_cold_boot_request

    @features('DualBank')
    @level('Functionality')
    def test_alternate_slot_request(self):
        """
        Check alternate slot request and check the image-to-boot-loader flags are cleared at each boot
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set alternate slot request flag")
        # --------------------------------------------------------------------------------------------------------------
        BootloaderImageCommunicationTestUtils.set_alternate_slot_request(test_case=self, alternate_slot_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set cold boot request flag")
        # --------------------------------------------------------------------------------------------------------------
        BootloaderImageCommunicationTestUtils.set_cold_boot_request(test_case=self, cold_boot_request=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Reset device (soft reset)")
        # --------------------------------------------------------------------------------------------------------------
        self.device_debugger.reset(soft_reset=True)
        time.sleep(self.config_manager.get_feature(self.config_manager.ID.STARTUP_TIME_COLD_BOOT) / 1000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get bootloader image communication bootloader to image flags")
        # --------------------------------------------------------------------------------------------------------------
        bl_to_img_flags = BootloaderImageCommunicationTestUtils.get_bl_to_img_flags(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check currently booted slot flag")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=BootImageCommunication.BlToImgFlags.BootedSlot.ALTERNATE_SLOT,
                         obtained=bl_to_img_flags.booted_slot,
                         msg="Currently booted slot should be alternate slot")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Get bootloader image communication image to bootloader flags")
        # --------------------------------------------------------------------------------------------------------------
        img_to_bl_flags = BootloaderImageCommunicationTestUtils.get_img_to_bl_flags(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the image-to-boot-loader flags are cleared at each boot")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=BootImageCommunication.ImgToBlFlags(),
                         obtained=img_to_bl_flags,
                         msg="Image to Bootloader flags should be cleared at each boot")

        self.testCaseChecked("FUN_DUAL_BANK_COM_0004")
    # end def test_alternate_slot_request
# end class BootloaderImageCommunicationFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
