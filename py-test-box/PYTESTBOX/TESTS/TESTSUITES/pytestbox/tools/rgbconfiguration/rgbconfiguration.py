#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.rgbconfiguration.rgbconfiguration
:brief: RGB effect configuration tool
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/07/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RGBConfigurationTools(DeviceBaseTestCase):
    """
    RGB configuration tools in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_reload_nvs = False

        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Delete RGB brightness chunk")
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.delete_led_brightness_chunk(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8071 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8071_index, self.feature_8071, _, _ = RGBEffectsTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS

        if self.config.F_HasEdgeLedDriver:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Enable Edge LED driver by writing the TDE block to the NVS")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            TdeAccessToNvmTestUtils.HIDppHelper.tde_clear_data(self)
            TdeAccessToNvmTestUtils.HIDppHelper.tde_write_data(
                test_case=self,
                starting_position=self.config.F_TdeEdgeLedDriverAddress,
                number_of_bytes_to_read_or_write=1,
                data_byte_0=HexList('AA')
            )
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Power OFF->ON DUT to enable Edge LED driver modification')
            # ----------------------------------------------------------------------------------------------------------
            self.power_slider_emulator.reset()
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        # noinspection PyBroadException
        with self.manage_kosmos_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'Stop RGB effect monitoring')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(self)
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class RGBConfigurationTools

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
