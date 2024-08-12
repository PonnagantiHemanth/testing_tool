#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8030.macrorecordkey
:brief: Validate HID++ 2.0 ``MacroRecordkey`` feature
:author: Zane Lu <zlu@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.root import Root
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.gaminggkeysutils import GamingGKeysTestUtils
from pytestbox.device.base.macrorecordkeyutils import MacroRecordkeyTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MacroRecordkeyTestCase(DeviceBaseTestCase):
    """
    Validate ``MacroRecordkey`` TestCases in Application mode
    """
    LED_TOGGLING_DELAY = 1

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        self.post_requisite_rechargeable = False
        self.external_power_source = None

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8030 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8030_index, self.feature_8030, _, _ = MacroRecordkeyTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.MACRORECORD_KEY

        self.feature_8010_index, self.feature_8010, _, _ = GamingGKeysTestUtils.HIDppHelper.get_parameters(
            test_case=self)
        if self.feature_8010_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Enable software control via x8010")
            # ----------------------------------------------------------------------------------------------------------
            GamingGKeysTestUtils.HIDppHelper.enable_software_control(test_case=self, enable=1)
        # end if

        self.feature_8100_index, self.feature_8100, _, _ = OnboardProfilesTestUtils.HIDppHelper.get_parameters(
            test_case=self)
        if self.feature_8100_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Set host mode via x8100")
            # ----------------------------------------------------------------------------------------------------------
            OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self,onboard_mode=2)
        # end if

        self.feature_8101_index, self.feature_8101, _, _ = ProfileManagementTestUtils.HIDppHelper.get_parameters(self)
        if self.feature_8101_index != Root.FEATURE_NOT_FOUND:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, "Set host mode via x8101")
            # ----------------------------------------------------------------------------------------------------------
            ProfileManagementTestUtils.HIDppHelper.get_set_mode(
                test_case=self, set_onboard_mode=1, onboard_mode=0, set_profile_mode=0, profile_mode=0)
        # end if
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_rechargeable:
                self.power_supply_emulator.recharge(enable=False)
                if self.external_power_source is not None:
                    DeviceTestUtils.ChargingHelper.exit_charging_mode(test_case=self,
                                                                      source=self.external_power_source)
                # end if
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class MacroRecordkeyTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
