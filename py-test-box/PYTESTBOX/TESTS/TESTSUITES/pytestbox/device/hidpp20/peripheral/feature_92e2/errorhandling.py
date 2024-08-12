#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_92e2.errorhandling
:brief: HID++ 2.0 ``TestKeysDisplay`` error handling test suite
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.testkeysdisplayutils import TestKeysDisplayTestUtils
from pytestbox.device.hidpp20.peripheral.feature_92e2.testkeysdisplay import TestKeysDisplayTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Gautham S B"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class TestKeysDisplayErrorHandlingTestCase(TestKeysDisplayTestCase):
    """
    Validate ``TestKeysDisplay`` errorhandling test cases
    """

    @features("Feature92E2")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_92e2.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetCapabilities request with a wrong function index: {function_index}")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.HIDppHelper.get_capabilities_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID], function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_92E2_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature92E2")
    @features("SupportSetKeyIcon")
    @level("ErrorHandling")
    def test_set_key_icon_with_invalid_row_col_code(self):
        """
        Validate sending Set Key Icon request with invalid values of row and column indexes returns an error
        """
        row_count = self.config.F_RowCount
        col_count = self.config.F_ColumnCount
        invalid_row_range = compute_wrong_range(value=list(range(row_count)), max_value=0xFE)
        invalid_column_range = compute_wrong_range(value=list(range(col_count)), max_value=0xFE)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting invalid values of row and column index")
        # --------------------------------------------------------------------------------------------------------------
        for row, col in zip(invalid_row_range, invalid_column_range):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyIcon request with selected row index = "
                                     f"{row} and column index = {col} value and check error code = INVALID_ARGUMENT "
                                     f"is received in response")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.HIDppHelper.set_key_icon_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT], key_row=row, key_column=col,
                icon_index=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_92E2_0002", _AUTHOR)
    # end def test_set_key_icon_with_invalid_row_col_code

    @features("Feature92E2")
    @features("SupportSetKeyIcon")
    @level("ErrorHandling")
    def test_set_key_icon_with_invalid_icon_index(self):
        """
        Validate sending Set Key Icon request with invalid values of icon indexes returns an error
        """
        icon_count = self.config.F_IconCount
        invalid_icon_index_range = compute_wrong_range(value=list(range(icon_count)), max_value=0xFF)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting invalid values of icon index")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_icon_index in invalid_icon_index_range:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SetKeyIcon request with selected icon index and check error code = "
                                     "INVALID_ARGUMENT is received in response")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.HIDppHelper.set_key_icon_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT], key_row=0, key_column=0,
                icon_index=invalid_icon_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_92E2_0003", _AUTHOR)
    # end def test_set_key_icon_with_invalid_icon_index

    @features("Feature92E2")
    @features("NoSupportSetKeyIcon")
    @level("ErrorHandling")
    def test_set_key_icon_returns_error_if_unsupported_by_device(self):
        """
        Validate sending Set Key Icon request returns an error if this API is not supported by device due to
        deprecation
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetKeyIcon request and check error code = INVALID_FUNCTION_ID is received")
        # --------------------------------------------------------------------------------------------------------------
        TestKeysDisplayTestUtils.HIDppHelper.set_key_icon_and_check_error(
            test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID], key_row=0, key_column=0, icon_index=0)

        self.testCaseChecked("ERR_92E2_0004", _AUTHOR)
    # end def test_set_key_icon_returns_error_if_unsupported_by_device

    @features("Feature92E2")
    @level("ErrorHandling")
    def test_set_key_calibration_offset_with_invalid_row_col_indexes(self):
        """
        Validate sending Set Key Calibration Offset API with invalid values of key_column and key_row parameters
        shall raise an error
        """
        row_count = self.config.F_RowCount
        col_count = self.config.F_ColumnCount
        invalid_row_range = compute_wrong_range(value=list(range(row_count)), max_value=0xFE)
        invalid_column_range = compute_wrong_range(value=list(range(col_count)), max_value=0xFE)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over several interesting invalid values of row and column index")
        # --------------------------------------------------------------------------------------------------------------
        for row, col in zip(invalid_row_range, invalid_column_range):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetKeyCalibrationOffset request with selected row index = {row} and "
                                     f"column index  = {col} and "
                                     "check error code = INVALID_ARGUMENT is received in response")
            # ----------------------------------------------------------------------------------------------------------
            TestKeysDisplayTestUtils.HIDppHelper.set_key_calibration_offset_and_check_error(
                test_case=self, error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
                key_row=row, key_column=col, x_offset=0, y_offset=0)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_92E2_0005", _AUTHOR)
    # end def test_set_key_calibration_offset_with_invalid_row_col_indexes
# end class TestKeysDisplayErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
