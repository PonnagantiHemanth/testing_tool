#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.hybridbutton.hyridbutton
:brief: Hid mouse hybrid button test case
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2024/02/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class HybridButtonTestCase(BaseTestCase):
    """
    Validate mouse hybrid button requirements
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.MODE_STATUS
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload device initial NV")
                # ------------------------------------------------------
                self.memory_manager.load_nvs(backup=True)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def set_mode_status_power_mode(self, power_mode):
        """
        Set hybrid switch power mode

        :param power_mode: Hybrid switch power mode
        :type power_mode: ``pyhid.hidpp.features.gaming.modestatus.ModeStatus.ModeStatus1.PowerMode``
        """
        if HexList(self.config.F_ModeStatus1).testBit(ModeStatus.ModeStatus1.POS.POWER_MODE) == power_mode:
            # Check if power_mode is the default mode
            return
        elif self.config.F_Enabled:
            # Check if feature 0x8090 (mode status) is enabled
            changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
            changed_mask_1 = (self.config.F_PowerSaveModeSupported +
                              (self.config.F_NonGamingSurfaceModeSupported << 1))
            mode_status_0 = ModeStatus.ModeStatus0.ENDURANCE_MODE
            mode_status_1 = ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE

            if power_mode == ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE and self.config.F_PowerSaveModeSupported:
                mode_status_1 = ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setModeStatus request with ModeStatus1 = {mode_status_1}, "
                                     f"ChangedMask1 = {changed_mask_1}")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            ModeStatusTestUtils.HIDppHelper.set_mode_status(test_case=self,
                                                            mode_status_0=mode_status_0,
                                                            mode_status_1=mode_status_1,
                                                            changed_mask_0=changed_mask_0,
                                                            changed_mask_1=changed_mask_1)
        else:
            raise ValueError(f"Unable to set power mode to {power_mode}, please ensure the setting is correct.")
        # end if
    # end def set_mode_status_power_mode
# end class HybridButtonTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
