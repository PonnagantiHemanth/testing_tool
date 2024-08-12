#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8090.errorhandling
:brief: HID++ 2.0 ``ModeStatus`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils
from pytestbox.device.hidpp20.gaming.feature_8090.modestatus import ModeStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusErrorHandlingTestCase(ModeStatusTestCase):
    """
    Validate ``ModeStatus`` errorhandling test cases
    """

    @features("Feature8090")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8090.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetModeStatus request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8090.get_mode_status_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8090_index)
            report.functionIndex = function_index

            ModeStatusTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8090_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8090")
    @level("ErrorHandling")
    def test_nvs_write_error(self):
        """
        Validate that non-volatile storage write error raises an error HW_ERROR(0x04)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "TODO")
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        self.testCaseChecked("ERR_8090_0002", _AUTHOR)
    # end def test_nvs_write_error

    @features("Feature8090")
    @level("ErrorHandling")
    def test_unsupported_mode_status(self):
        """
        Validate that an error INVALID_ARGUMENT(0x02) should be raised while sending setModeStatus request if the DUT
        not support ModeStatus0 or 1
        """
        self.post_requisite_reload_nvs = True
        changed_mask_0 = 1 if not self.config.F_ModeStatus0ChangedBySw else 0
        changed_mask_1 = 1 if not self.config.F_PowerSaveModeSupported else 0
        mode_status_0 = ModeStatus.ModeStatus0.ENDURANCE_MODE
        mode_status_1 = ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setModeStatus request with ModeStatus0 = {mode_status_0}, "
                                 f"ModeStatus = {mode_status_1}, ChangedMask_0 = {changed_mask_0} "
                                 f"and ChangedMask_1 = {changed_mask_1}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8090.set_mode_status_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_8090_index,
            mode_status_0=mode_status_0,
            mode_status_1=mode_status_1,
            changed_mask_0=changed_mask_0,
            changed_mask_1=changed_mask_1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) error code returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        ModeStatusTestUtils.HIDppHelper.send_report_wait_error(test_case=self,
                                                               report=report,
                                                               error_codes=[ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_8090_0003", _AUTHOR)
    # end def test_unsupported_mode_status
# end class ModeStatusErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
