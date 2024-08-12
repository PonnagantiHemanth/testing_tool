#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.errorhandling
:brief: HID++ 2.0 ``MultiRoller`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.keyboard.multiroller import RollerMode
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multirollerutils import MultiRollerTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4610.multiroller import MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerErrorHandlingTestCase(MultiRollerTestCase):
    """
    Validate ``MultiRoller`` errorhandling test cases
    """

    @features("Feature4610")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_4610.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4610_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature4610")
    @level("ErrorHandling")
    def test_invalid_roller_id_in_get_roller_capabilities_request(self):
        """
        Validate invalid roller_id shall raise an error when sending GetRollerCapabilities request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: wrong_roller_id in range({self.config.F_NumRollers}, 0xF)")
        # --------------------------------------------------------------------------------------------------------------
        for wrong_roller_id in range(self.config.F_NumRollers, 0xF + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetRollerCapabilities request with roller_id = {wrong_roller_id} and "
                                     "validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.get_roller_capabilities_and_check_error(
                test_case=self, roller_id=wrong_roller_id, error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4610_0002", _AUTHOR)
    # end def test_invalid_roller_id_in_get_roller_capabilities_request

    @features("Feature4610")
    @level("ErrorHandling")
    def test_invalid_roller_id_in_get_mode(self):
        """
        Validate invalid roller_id shall raise an error when sending GetMode request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: wrong_roller_id in range({self.config.F_NumRollers}, 0xF)")
        # --------------------------------------------------------------------------------------------------------------
        for wrong_roller_id in range(self.config.F_NumRollers, 0xF + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetMode request with roller_id = {wrong_roller_id} and "
                                     "validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.get_mode_and_check_error(test_case=self,
                                                                      roller_id=wrong_roller_id,
                                                                      error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4610_0003", _AUTHOR)
    # end def test_invalid_roller_id_in_get_mode

    @features("Feature4610")
    @level("ErrorHandling")
    def test_invalid_roller_id_in_set_mode(self):
        """
        Validate invalid roller_id shall raise an error when sending SetMode request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop: wrong_roller_id in range({self.config.F_NumRollers}, 0xF)")
        # --------------------------------------------------------------------------------------------------------------
        for wrong_roller_id in range(self.config.F_NumRollers, 0xF + 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetMode request with roller_id = {wrong_roller_id} and "
                                     "validate INVALID_ARGUMENT(0x02) error code")
            # ----------------------------------------------------------------------------------------------------------
            MultiRollerTestUtils.HIDppHelper.set_mode_and_check_error(test_case=self,
                                                                      roller_id=wrong_roller_id,
                                                                      divert=RollerMode.DEFAULT_MODE,
                                                                      error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4610_0004", _AUTHOR)
    # end def test_invalid_roller_id_in_set_mode
# end class MultiRollerErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
