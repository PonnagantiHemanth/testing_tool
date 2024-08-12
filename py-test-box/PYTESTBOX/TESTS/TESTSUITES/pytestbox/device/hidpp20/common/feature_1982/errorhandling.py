#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1982.errorhandling
:brief: HID++ 2.0 ``Backlight`` error handling test suite
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.backlightutils import BacklightTestUtils
from pytestbox.device.hidpp20.common.feature_1982.backlight import BacklightTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Anil Gadad"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightErrorHandlingTestCase(BacklightTestCase):
    """
    Validate ``Backlight`` errorhandling test cases
    """

    @features("Feature1982")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1982.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetBacklightConfig request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1982.get_backlight_config_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1982_index)
            report.functionIndex = function_index

            BacklightTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1982_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1982v3+")
    @level("ErrorHandling")
    def test_set_temporary_manual_mode_by_sw(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2) while set bcklMode =
        Temporary Manual Mode
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set bcklMode = Temporary manual mode (2)")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.switch_backlight_mode(self, Backlight.Options.TEMPORARY_MANUAL_MODE),
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0002", _AUTHOR)
    # end def test_set_temporary_manual_mode_by_sw

    @features("Feature1982v3+")
    @features("BacklightModeSupported")
    @level("ErrorHandling")
    def test_set_no_backlight_mode_selected_but_device_supported(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2) while set bcklMode = 0 but autoMode_s,
        permManualMode_s or tempManualMode_s are set.
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set bcklMode = No backlight mode selected (0) but device supports backlight modes")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.switch_backlight_mode(self, Backlight.Options.NO_BACKLIGHT_MODE_SELECTED),
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0003", _AUTHOR)
    # end def test_set_no_backlight_mode_selected_but_device_supported

    @features("Feature1982v3+")
    @features("NoFeature1982RequiredOptions", Backlight.SupportedOptionsMask.AUTO_MODE_S)
    @level("ErrorHandling")
    def test_set_auto_backlight_mode_but_device_not_supported(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2) while set bcklMode = 1 (auto)
        but autoMode_s = 0.
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set bcklMode = ALS Automatic mode (1) but device doesn't support it")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.switch_backlight_mode(self, Backlight.Options.AUTOMATIC_MODE),
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0004", _AUTHOR)
    # end def test_set_auto_backlight_mode_but_device_not_supported

    @features("Feature1982v3+")
    @features("NoFeature1982RequiredOptions", Backlight.SupportedOptionsMask.PERM_MANUAL_MODE_S)
    @level("ErrorHandling")
    def test_set_permanent_manual_mode_but_device_not_supported(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2) while set bcklMode = 3 (permanent)
        but permManualMode_s = 0.
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set bcklMode = Permanent manual mode (3) but device doesn't support it")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.switch_backlight_mode(self, Backlight.Options.PERMANENT_MANUAL_MODE),
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0005", _AUTHOR)
    # end def test_set_permanent_manual_mode_but_device_not_supported

    @features("Feature1982v3+")
    @features("NoFeature1982RequiredOptions", Backlight.SupportedOptionsMask.WOW_S)
    @level("ErrorHandling")
    def test_enable_wow_but_device_not_supported(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2) while set wow = 1 (enable) but wow_s = 0.
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set WOW = enable (1) but device doesn't support it")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.get_default_options(self) | Backlight.Options.WOW,
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0006", _AUTHOR)
    # end def test_enable_wow_but_device_not_supported

    @features("Feature1982v3+")
    @features("NoFeature1982RequiredOptions", Backlight.SupportedOptionsMask.CROWN_S)
    @level("ErrorHandling")
    def test_enable_crown_but_device_not_supported(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2)
        while set crown = 1 (enable) but crown_s = 0.
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set CROWN = enable (1) but device doesn't support it")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.get_default_options(self) | Backlight.Options.CROWN,
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0007", _AUTHOR)
    # end def test_enable_crown_but_device_not_supported

    @features("Feature1982v3+")
    @features("NoFeature1982RequiredOptions", Backlight.SupportedOptionsMask.PWR_SAVE_S)
    @level("ErrorHandling")
    def test_enable_power_safe_but_device_not_supported(self):
        """
        [Since v3] Validate the device shall send an error INVALID_ARGUMENT(2)
        while set pwrSave = 1 (enable) but cpwrSave_s = 0.
        """
        self.post_requisite_reload_nvs = True
        software_id = 0xF
        curr_duration_hands_out = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_hands_in = Numeral(2, byteCount=2, littleEndian=True)
        curr_duration_powered = Numeral(2, byteCount=2, littleEndian=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set PwrSave = enable (1) but device doesn't support it")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1982.set_backlight_config_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1982_index,
            software_id=software_id,
            configuration=Backlight.Configuration.ENABLE,
            options=BacklightTestUtils.get_default_options(self) | Backlight.Options.PWR_SAVE,
            backlight_effect=Backlight.BacklightEffect.CURRENT_EFFECT,
            current_backlight_level=Backlight.CurrentLevel.CURRENT_LEVEL_2,
            curr_duration_hands_out=curr_duration_hands_out,
            curr_duration_hands_in=curr_duration_hands_in,
            curr_duration_powered=curr_duration_powered)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait HID++ 2.0 Error message then check error code = INVALID_ARGUMENT(2)")
        # --------------------------------------------------------------------------------------------------------------
        BacklightTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1982_0008", _AUTHOR)
    # end def test_enable_power_safe_but_device_not_supported
# end class BacklightErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
