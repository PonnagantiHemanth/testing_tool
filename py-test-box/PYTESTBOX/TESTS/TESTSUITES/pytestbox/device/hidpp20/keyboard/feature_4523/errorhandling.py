#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4523.errorhandling
:brief: HID++ 2.0 ``DisableControlsByCIDX`` error handling test suite
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablecontrolsbycidxutils import DisableControlsByCIDXTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4523.disablecontrolsbycidx import DisableControlsByCIDXTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Zane Lu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DisableControlsByCIDXErrorHandlingTestCase(DisableControlsByCIDXTestCase):
    """
    Validate ``DisableControlsByCIDX`` errorhandling test cases
    """

    @features("Feature4523")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_4523.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetDisabledControls request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            DisableControlsByCIDXTestUtils.HIDppHelper.set_disabled_controls_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4523_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature4523v1")
    @features("NoFeature4523GameModeSupported")
    @level("ErrorHandling")
    def test_check_invalid_arguments_for_set_power_on_params_without_poweron_game_mode_support(self):
        """
        Check INVALID_ARGUMENT error id from getSetPowerOnParams
        if getCapabilities.supported_poweron_params.poweron_game_mode = 0,
        that is, attempt to set an unsupported poweron parameter.
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getSetPowerOnParams request with invalid parameters")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
            poweron_game_mode_lock_valid=False,
            poweron_game_mode_valid=True,
            poweron_game_mode_lock=False,
            poweron_game_mode=True)
        self.testCaseChecked("ERR_4523_0002", _AUTHOR)
    # end def test_check_invalid_arguments_for_set_power_on_params_without_poweron_game_mode_support

    @features("Feature4523v1")
    @features("NoFeature4523GameModeLockSupported")
    @level("ErrorHandling")
    def test_check_invalid_arguments_for_set_power_on_params_without_poweron_game_mode_lock_support(self):
        """
        check INVALID_ARGUMENT error id from getSetPowerOnParams
        if getCapabilities.supported_poweron_params.poweron_game_mode_lock = 0,
        that is, attempt to set an unsupported poweron parameter
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send getSetPowerOnParams request with invalid parameters")
        # --------------------------------------------------------------------------------------------------------------
        DisableControlsByCIDXTestUtils.HIDppHelper.get_set_power_on_params_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
            poweron_game_mode_lock_valid=True,
            poweron_game_mode_valid=False,
            poweron_game_mode_lock=True,
            poweron_game_mode=False)
        self.testCaseChecked("ERR_4523_0003", _AUTHOR)
    # end def test_check_invalid_arguments_for_set_power_on_params_without_poweron_game_mode_lock_support
# end class DisableControlsByCIDXErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
