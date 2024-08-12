#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1801.errorhandling
:brief: HID++ 2.0 ``ManufacturingMode`` error handling test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.manufacturingmodeutils import ManufacturingModeTestUtils
from pytestbox.device.hidpp20.common.feature_1801.manufacturingmode import ManufacturingModeTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"
_LOOP_START_RESERVED = "Test loop over reserved range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ManufacturingModeErrorHandlingTestCase(ManufacturingModeTestCase):
    """
    Validate ``ManufacturingMode`` errorhandling test cases
    """

    @features("Feature1801")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1801.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetManufacturingMode request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID],
                manufacturing_mode=manufacturing_mode,
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1801_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1801")
    @level("ErrorHandling")
    def test_set_manufacturing_mode_reserved(self):
        """
        Validate ``SetManufacturingMode`` reserved bits could not be set. An invalid argument error shall be returned by
        the firmware if the manufacturingMode byte is above the value of 1.

        [0] setManufacturingMode(manufacturingMode) -> None
        """
        manufacturing_mode = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_RESERVED)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_1801.set_manufacturing_mode_cls
        for reserved in compute_wrong_range(0, max_value=(1 << request_cls.LEN.RESERVED) - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetManufacturingMode request with reserved: {reserved}")
            LogHelper.log_check(self, f"Check INVALID_ARGUMENT (2) Error Code returned by the device")
            # ----------------------------------------------------------------------------------------------------------
            ManufacturingModeTestUtils.HIDppHelper.set_manufacturing_mode_and_check_error(
                test_case=self,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                manufacturing_mode=manufacturing_mode,
                reserved=reserved)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1801_0002", _AUTHOR)
    # end def test_set_manufacturing_mode_reserved
# end class ManufacturingModeErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
