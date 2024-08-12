#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8090.business
:brief: HID++ 2.0 ``ModeStatus`` business test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.tools.numeral import to_int
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8090.modestatus import ModeStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusBusinessTestCase(ModeStatusTestCase):
    """
    Validate ``ModeStatus`` business test cases
    """

    @features("Feature8090")
    @features("Feature1830")
    @level("Business")
    def test_mode_status_settings_kept_after_deep_sleep(self):
        """
        Validate that ModeStatus0 and ModeStatus1 will be kept after the DUT entered deep-sleep mode
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request to change the device supported ModeStatus ")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.set_mode_status(test_case=self,
                                                                   mode_status_0=mode_status_0,
                                                                   mode_status_1=mode_status_1,
                                                                   changed_mask_0=changed_mask_0,
                                                                   changed_mask_1=changed_mask_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait setModeStatus response and check its inputs fields are as expected")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.MessageChecker.check_fields(
            self, response, self.feature_8090.set_mode_status_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check the supported ModeStatus has been changed")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0_bit_map,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(mode_status_0=mode_status_0)),
            "mode_status_1": (checker.check_mode_status_1_bit_map,
                              ModeStatusTestUtils.ModeStatus1Checker.get_check_map(mode_status_1=mode_status_1))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetPowerMode request with PowerModeNumber = 0x03 (deep-sleep mode)")
        # --------------------------------------------------------------------------------------------------------------
        PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Perform an user action to wake up the device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check the supported ModeStatus is unchanged")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0_bit_map,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(mode_status_0=mode_status_0)),
            "mode_status_1": (checker.check_mode_status_1_bit_map,
                              ModeStatusTestUtils.ModeStatus1Checker.get_check_map(mode_status_1=mode_status_1))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        self.testCaseChecked("BUS_8090_0001", _AUTHOR)
    # end def test_mode_status_settings_kept_after_deep_sleep

    @features("Feature8090")
    @level('Business', 'SmokeTests')
    def test_optical_switch_is_working_in_low_latency_mode(self):
        """
        Validate the optical switch is working while the ModeStatus1 is set to Low latency mode, and the optical
        switch will not work while the ModeStatus1 is set to Power save mode
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = ModeStatus.ModeStatus0.ENDURANCE_MODE
        mode_status_1 = ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus1 = 0, ChangedMask1 = 1")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.set_mode_status(test_case=self,
                                                                   mode_status_0=mode_status_0,
                                                                   mode_status_1=mode_status_1,
                                                                   changed_mask_0=changed_mask_0,
                                                                   changed_mask_1=changed_mask_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait setModeStatus response and check its inputs fields are as expected")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.MessageChecker.check_fields(
            self, response, self.feature_8090.set_mode_status_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus1 equals 0 (Low latency mode)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0_bit_map,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(mode_status_0=mode_status_0)),
            "mode_status_1": (checker.check_mode_status_1_bit_map,
                              ModeStatusTestUtils.ModeStatus1Checker.get_check_map(mode_status_1=mode_status_1))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check optical switch is working (Check the GPIO status or LED status)")
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus1 = 1, ChangedMask1 = 1")
        # --------------------------------------------------------------------------------------------------------------
        mode_status_1 = ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE
        response = ModeStatusTestUtils.HIDppHelper.set_mode_status(test_case=self,
                                                                   mode_status_0=mode_status_0,
                                                                   mode_status_1=mode_status_1,
                                                                   changed_mask_0=changed_mask_0,
                                                                   changed_mask_1=changed_mask_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait setModeStatus response and check its inputs fields are as expected")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.MessageChecker.check_fields(
            self, response, self.feature_8090.set_mode_status_response_cls, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus1 equals 1 (Power save mode)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0_bit_map,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(mode_status_0=mode_status_0)),
            "mode_status_1": (checker.check_mode_status_1_bit_map,
                              ModeStatusTestUtils.ModeStatus1Checker.get_check_map(mode_status_1=mode_status_1))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check optical switch is not working (Check the GPIO status or LED status)")
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        self.testCaseChecked("BUS_8090_0002", _AUTHOR)
    # end def test_optical_switch_is_working_in_low_latency_mode
# end class ModeStatusBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
