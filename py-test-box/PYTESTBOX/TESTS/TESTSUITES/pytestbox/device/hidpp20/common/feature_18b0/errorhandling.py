#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_18b0.errorhandling
:brief: HID++ 2.0 ``StaticMonitorMode`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorMode
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.staticmonitormodeutils import StaticMonitorModeTestUtils
from pytestbox.device.hidpp20.common.feature_18b0.staticmonitormode import StaticMonitorModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class StaticMonitorModeErrorHandlingTestCase(StaticMonitorModeTestCase):
    """
    Validate ``StaticMonitorMode`` errorhandling test cases
    """

    @features("Feature18B0")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_18b0.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_18b0.set_monitor_mode_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_18b0_index,
                mode=HexList(Numeral(StaticMonitorMode.OFF)))
            report.function_index = function_index

            StaticMonitorModeTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_18B0_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature18B0")
    @features("Mice")
    @level("ErrorHandling")
    @services("OpticalSensor")
    def test_mouse_set_monitor_mode_invalid_output_xy(self):
        """
        Validate invalid output - X & Y (mouse)

        [0] setMonitorMode(mode)
        """
        raise NotImplementedError("to be implemented when @services('OpticalSensor') is available")
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with a mode: 2")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Set xy_motion(dx=0x8000) using OpticalXyDisplacmentInterface")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 0 (OFF)")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetMonitorModeResponse fields")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_18B0_0002", _AUTHOR)
    # end def test_mouse_set_monitor_mode_invalid_output_xy

    @features("Feature18B0")
    @level("ErrorHandling")
    def test_set_monitor_mode_invalid_parameter_mode(self):
        """
        Validate invalid parameter - mode (keyboard or mouse)

        [0] setMonitorMode(mode)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over mode invalid range [0x6..0xFF]")
        # --------------------------------------------------------------------------------------------------------------
        for mode in compute_sup_values(StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a wrong mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_18b0.set_monitor_mode_cls(device_index=self.device_index,
                                                            feature_index=self.feature_18b0_index,
                                                            mode=HexList(mode))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT error code")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_18B0_0003", _AUTHOR)
    # end def test_set_monitor_mode_invalid_parameter_mode

    @features("Feature18B0")
    @level("ErrorHandling")
    def test_set_monitor_mode_unsupported_parameter_mode(self):
        """
        Validate unsupported "mode" parameter

        [0] setMonitorMode(mode)
        """
        all_modes = {StaticMonitorMode.KBD_ON: self.config.F_KeyboardMode,
                     StaticMonitorMode.MOUSE_ON: self.config.F_Mice,
                     StaticMonitorMode.ENHANCED_KBD_ON: self.config.F_EnhancedKeyboardMode,
                     StaticMonitorMode.KBD_LARGER_MATRIX: self.config.F_KeyboardWithLargerMatrixMode,
                     StaticMonitorMode.ENHANCED_KBD_LARGER_MATRIX: self.config.F_EnhancedKeyboardWithLargerMatrixMode}

        wrong_modes = [value for value, mode in all_modes.items() if not mode]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test loop over mode invalid range {wrong_modes}")
        # --------------------------------------------------------------------------------------------------------------
        for mode in wrong_modes:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMonitorMode request with a wrong mode: {mode}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_18b0.set_monitor_mode_cls(device_index=self.device_index,
                                                            feature_index=self.feature_18b0_index,
                                                            mode=HexList(mode))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT error code")
            # ----------------------------------------------------------------------------------------------------------
            StaticMonitorModeTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_18B0_0004", _AUTHOR)
    # end def test_set_monitor_mode_unsupported_parameter_mode

    @features("Feature18B0")
    @level("ErrorHandling")
    def test_set_monitor_mode_after_disable_hidden_feature(self):
        """
        Check NOT_ALLOWED error is raised if hidden feature is disabled

        [0] setMonitorMode(mode)
        """
        mode = StaticMonitorMode.OFF
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Disable hidden feature")
        # --------------------------------------------------------------------------------------------------------------
        DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.disable_features(test_case=self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetMonitorMode request with mode: 0")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_18b0.set_monitor_mode_cls(device_index=self.device_index,
                                                        feature_index=self.feature_18b0_index,
                                                        mode=HexList(mode))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Validate NOT_ALLOWED error code")
        # --------------------------------------------------------------------------------------------------------------
        StaticMonitorModeTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_18B0_0006", _AUTHOR)
    # end def test_set_monitor_mode_after_disable_hidden_feature
# end class StaticMonitorModeErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
