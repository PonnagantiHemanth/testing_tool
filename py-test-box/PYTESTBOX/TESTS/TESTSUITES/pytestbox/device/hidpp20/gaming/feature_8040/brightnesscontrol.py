#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.brightnesscontrol
:brief: Validate HID++ 2.0 ``BrightnessControl`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlTestCase(DeviceBaseTestCase):
    """
    Validate ``BrightnessControl`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        self.post_requisite_discharge_super_cap = False
        self.post_requisite_rechargeable = False
        self.post_requisite_exit_ble_channel = False
        self.external_power_source = None

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8040 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8040_index, self.feature_8040, _, _ = BrightnessControlTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get calibration factor')
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        self.calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL
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
            if self.post_requisite_exit_ble_channel:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Exit BLE channel")
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_ble_channel(self)
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            if self.external_power_source is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, f"Exit {self.external_power_source!s} charging mode")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self,
                                                                  source=self.external_power_source)
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

        with self.manage_post_requisite():
            if self.post_requisite_discharge_super_cap:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Discharge the supercap')
                # ------------------------------------------------------------------------------------------------------
                self.device.turn_off_crush_pad_charging_emulator()
                self.power_supply_emulator.turn_on(voltage=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)
                sleep(UnifiedBatteryTestUtils.DISCHARGE_SUPERCAP_TIME)
                self.post_requisite_discharge_super_cap = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class BrightnessControlTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
