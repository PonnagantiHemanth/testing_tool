#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8071.rgbeffects
:brief: Validate HID++ 2.0 ``RGBEffects`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RGBEffectsTestCase(DeviceBaseTestCase):
    """
    Validate ``RGBEffects`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_reload_nvs = False
        self.post_requisite_turn_off_usb_charging_cable = False
        self.post_requisite_power_on_device = False

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

        with self.manage_kosmos_post_requisite():
            if self.post_requisite_power_on_device:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Power ON the DUT')
                # ------------------------------------------------------------------------------------------------------
                self.power_slider_emulator.power_on()
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            if self.post_requisite_turn_off_usb_charging_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Stop device charging")
                # ------------------------------------------------------------------------------------------------------
                if self.power_supply_emulator is not None:
                    self.power_supply_emulator.recharge(enable=False)
                # end if
                self.device.turn_off_usb_charging_cable()
                self.post_requisite_turn_off_usb_charging_cable = False
            # end if
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
# end class RGBEffectsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
