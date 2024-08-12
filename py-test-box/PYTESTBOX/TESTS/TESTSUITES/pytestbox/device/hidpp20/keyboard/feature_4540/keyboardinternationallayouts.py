#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4540.keyboardinternationallayouts
:brief: Validate HID++ 2.0 ``KeyboardInternationalLayouts`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.keyboardinternationallayoutsutils import KeyboardInternationalLayoutsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayoutsTestCase(DeviceBaseTestCase):
    """
    Validate ``KeyboardInternationalLayouts`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Post requisite flags definition
        self.post_requisite_set_nominal_voltage = False
        self.post_requisite_unplug_usb_cable = False

        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4540 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_4540_index, self.feature_4540, self.device_index, _ = \
            KeyboardInternationalLayoutsTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.KEYBOARD.KEYBOARD_INTERNATIONAL_LAYOUTS
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """

        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with

        with self.manage_kosmos_post_requisite():
            if self.post_requisite_set_nominal_voltage:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Put back nominal voltage")
                # ------------------------------------------------------------------------------------------------------
                self.power_supply_emulator.set_voltage(voltage=self.f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage)
                self.post_requisite_set_nominal_voltage = False
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_unplug_usb_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Exit charging mode and turn off USB charging")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.ChargingHelper.exit_charging_mode(self)
                self.post_requisite_unplug_usb_cable = False
            # end if
        # end with
        
        super().tearDown()
    # end def tearDown
# end class KeyboardInternationalLayoutsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
