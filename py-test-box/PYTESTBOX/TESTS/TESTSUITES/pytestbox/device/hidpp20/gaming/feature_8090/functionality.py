#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8090.functionality
:brief: HID++ 2.0 ``ModeStatus`` functionality test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features, services
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.tools.numeral import to_int
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.hidpp20.gaming.feature_8090.modestatus import ModeStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusFunctionalityTestCase(ModeStatusTestCase):
    """
    Validate ``ModeStatus`` functionality test cases
    """

    @features("Feature8090")
    @level("Functionality")
    def test_mode_status_0_set_by_sw(self):
        """
        Validate ModeStatus0 can be set by setModeStatus, if the device has the capability
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = to_int(self.config.F_ModeStatus1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus0 = 1, ChangedMask0 = 1")
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
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 1(Performance mode)")
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
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus0 = 0, ChangedMask0 = 1")
        # --------------------------------------------------------------------------------------------------------------
        mode_status_0 = ModeStatus.ModeStatus0.ENDURANCE_MODE
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
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 0(Endurance mode)")
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

        self.testCaseChecked("FUN_8090_0001", _AUTHOR)
    # end def test_mode_status_0_set_by_sw

    @features("Feature8090")
    @level("Functionality")
    def test_mode_status_1_set_by_sw(self):
        """
        Validate ModeStatus1 can be set by setModeStatus, if the device has the capability
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = ModeStatus.ModeStatus0.ENDURANCE_MODE if changed_mask_0 \
            else to_int(self.config.F_ModeStatus0)
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setModeStatus request with ModeStatus1 = {mode_status_1}, "
                                 f"ChangedMask1 = {changed_mask_1}")
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
        LogHelper.log_check(self, f"Wait getModeStatus response and check ModeStatus1 equals {mode_status_1}")
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
        LogHelper.log_step(self, f"Send setModeStatus request with ModeStatus1 = {to_int(self.config.F_ModeStatus1)},"
                                 f" ChangedMask1 = {changed_mask_1}")
        # --------------------------------------------------------------------------------------------------------------
        mode_status_1 = to_int(self.config.F_ModeStatus1)
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
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus1 equals 1(Power save mode)")
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

        self.testCaseChecked("FUN_8090_0002", _AUTHOR)
    # end def test_mode_status_1_set_by_sw

    @features("Feature8090")
    @features("Feature8090HwSwitch")
    @level("Functionality")
    @services("PowerSwitch")
    def test_mode_status_0_set_by_hw(self):
        """
        Validate ModeStatus0 can be set by HW switch, and the DevCapability is not going to change after the ModeStatus0
         is changed by HW switch.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set ModeStatus0 = 1 (Performance mode) by HW switch")
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 1 (Performance mode)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0_bit_map,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(
                                  mode_status_0=ModeStatus.ModeStatus0.PERFORMANCE_MODE))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait modeStatusBroadcasting event and check ModeStatus0 equals 1 (Performance mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.mode_status_broadcasting_event(test_case=self)
        checker = ModeStatusTestUtils.ModeStatusBroadcastingEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(
                                  mode_status_0=ModeStatus.ModeStatus0.PERFORMANCE_MODE))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDevConfig request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_dev_config(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getDevConfig response and check DevConfig are as expected (Product capability)")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.GetDevConfigResponseChecker.check_fields(
            self, response, self.feature_8090.get_dev_config_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set ModeStatus0 = 0 (Endurance mode) by HW switch")
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 0 (Endurance mode)")
        # --------------------------------------------------------------------------------------------------------------
        checker = ModeStatusTestUtils.GetModeStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0_bit_map,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(
                                  mode_status_0=ModeStatus.ModeStatus0.PERFORMANCE_MODE))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait modeStatusBroadcasting event and check ModeStatus0 equals 0 (Endurance mode)")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.mode_status_broadcasting_event(test_case=self)
        checker = ModeStatusTestUtils.ModeStatusBroadcastingEventChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "mode_status_0": (checker.check_mode_status_0,
                              ModeStatusTestUtils.ModeStatus0Checker.get_check_map(
                                  mode_status_0=ModeStatus.ModeStatus0.ENDURANCE_MODE))
        })
        checker.check_fields(self, response, self.feature_8090.get_mode_status_response_cls, check_map)

        self.testCaseChecked("FUN_8090_0003", _AUTHOR)
    # end def test_mode_status_0_set_by_hw

    @features("Feature8090")
    @features("Wireless")
    @level("Functionality")
    @services("PowerSupply")
    def test_mode_status_0_setting_kept_after_restart(self):
        """
        Validate ModeStatus0 will be kept after power reset device
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = to_int(self.config.F_ModeStatus1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus0 = 1, ChangedMask0 = 1")
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
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 1 (Performance mode)")
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
        LogHelper.log_step(self, "Power OFF -> ON the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 1 (Performance mode)")
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

        self.testCaseChecked("FUN_8090_0004", _AUTHOR)
    # end def test_mode_status_0_setting_kept_after_restart

    @features("Feature8090")
    @features("Wireless")
    @level("Functionality")
    @services("PowerSupply")
    @services("PowerSwitch")
    def test_mode_status_0_setting_kept_after_restart_by_power_switch(self):
        """
        Validate ModeStatus0 will be kept after power reset device by power switch
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = (0xFF - to_int(self.config.F_ModeStatus0)) & changed_mask_0
        mode_status_1 = to_int(self.config.F_ModeStatus1)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setModeStatus request with ModeStatus0 = 1, ChangedMask0 = 1")
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
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 1 (Performance mode)")
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
        LogHelper.log_step(self, "Switch OFF -> ON the device")
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.reset()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        response = ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait getModeStatus response and check ModeStatus0 equals 1 (Performance mode)")
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

        self.testCaseChecked("FUN_8090_0005", _AUTHOR)
    # end def test_mode_status_0_setting_kept_after_restart_by_power_switch

    @features("Feature8090")
    @features("Wireless")
    @level("Functionality")
    @services("PowerSupply")
    def test_mode_status_1_setting_kept_after_restart(self):
        """
        Validate ModeStatus1 will be kept after power reset device
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = to_int(self.config.F_ModeStatus0)
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
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
        LogHelper.log_step(self, "Power OFF -> ON the device")
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)

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

        self.testCaseChecked("FUN_8090_0006", _AUTHOR)
    # end def test_mode_status_1_setting_kept_after_restart

    @features("Feature8090")
    @features("Wireless")
    @level("Functionality")
    @services("PowerSupply")
    @services("PowerSwitch")
    def test_mode_status_1_setting_kept_after_restart_by_power_switch(self):
        """
        Validate ModeStatus1 will be kept after power reset device by power switch
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = self.config.F_PowerSaveModeSupported + \
            (self.config.F_NonGamingSurfaceModeSupported << 1)
        mode_status_0 = to_int(self.config.F_ModeStatus0)
        mode_status_1 = (0xFF - to_int(self.config.F_ModeStatus1)) & changed_mask_1
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
        ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

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
        LogHelper.log_step(self, "Switch OFF -> ON the device")
        # --------------------------------------------------------------------------------------------------------------
        self.power_slider_emulator.reset()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getModeStatus request")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.HIDppHelper.get_mode_status(test_case=self)

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

        self.testCaseChecked("FUN_8090_0007", _AUTHOR)
    # end def test_mode_status_1_setting_kept_after_restart_by_power_switch
# end class ModeStatusFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
