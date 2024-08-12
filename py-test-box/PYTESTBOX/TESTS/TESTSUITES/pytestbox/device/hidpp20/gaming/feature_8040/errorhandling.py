#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.errorhandling
:brief: HID++ 2.0 ``BrightnessControl`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import sample

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV1
from pyhid.hidpp.features.gaming.brightnesscontrol import IlluminationState
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.brightnesscontrolutils import BrightnessControlTestUtils
from pytestbox.device.hidpp20.gaming.feature_8040.brightnesscontrol import BrightnessControlTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlErrorHandlingTestCase(BrightnessControlTestCase):
    """
    Validate ``BrightnessControl`` errorhandling test cases
    """

    @features("Feature8040")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8040.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetInfo request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.get_info_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8040_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8040")
    @level("ErrorHandling")
    def test_invalid_min_max_brightness(self):
        """
        Validate Invalid Argument (0x02) error is sent when the requested brightness is less than the minBrightness
        or larger than the maxBrightness
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: invalid_brightness in range(0, minBrightness)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_brightness in range(0, self.config.F_MinBrightness):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={invalid_brightness}")
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness_and_check_error(
                test_case=self, brightness=invalid_brightness, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop: invalid_brightness in range(maxBrightness + 1, 0xFFFF)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_brightness in sample(list(range(self.config.F_MaxBrightness + 1, 0xFFFF)), 10) + \
                [self.config.F_MaxBrightness + 1, 0xFFFF]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setBrightness request with brightness={invalid_brightness}")
            LogHelper.log_check(self, "Validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            BrightnessControlTestUtils.HIDppHelper.set_brightness_and_check_error(
                test_case=self, brightness=invalid_brightness, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_8040_0002", _AUTHOR)
    # end def test_invalid_min_max_brightness

    @features("Feature8040v1")
    @features("NoRequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("ErrorHandling")
    def test_not_allowed_get_illumination_request(self):
        """
        Validate Not Allowed (0x05) error is sent when sending getIllumination request and the illumination
        capability is not supported by the device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send getIllumination request")
        LogHelper.log_check(self, "Validate NOT_ALLOWED(0x05) error code")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.get_illumination_and_check_error(
            test_case=self, error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_8040_0003", _AUTHOR)
    # end def test_not_allowed_get_illumination_request

    @features("Feature8040v1")
    @features("NoRequiredBrightnessCapability", CapabilitiesV1.POS.ILLUMINATION)
    @level("ErrorHandling")
    def test_not_allowed_set_illumination_request(self):
        """
        Validate Not Allowed (0x05) error is sent when sending setIllumination request and the illumination
        capability is not supported by the device
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send setIllumination request")
        LogHelper.log_check(self, "Validate NOT_ALLOWED(0x05) error code")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_illumination_and_check_error(
            test_case=self, state=IlluminationState.OFF, error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_8040_0004", _AUTHOR)
    # end def test_not_allowed_set_illumination_request
# end class BrightnessControlErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
