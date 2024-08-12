#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1eb0.errorhandling
:brief: HID++ 2.0 ``TdeAccessToNvm`` error handling test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils
from pytestbox.device.hidpp20.common.feature_1eb0.tdeaccesstonvm import TdeAccessToNvmTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmErrorHandlingTestCase(TdeAccessToNvmTestCase):
    """
    Validate ``TdeAccessToNvm`` errorhandling test cases
    """
    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_tde_write_data_wrong_starting_position(self):
        """
        Validates write data with wrong starting position
        """
        params = self.get_parameters(starting_position=self.tde_max_size + 1,
                                     write_dict=self.get_write_parameters(err_code=ErrorCodes.INVALID_ARGUMENT))
        self.process_api(params)

        self.testCaseChecked("ERR_1EB0_0001", _AUTHOR)
    # end def test_wrong_starting_position

    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_tde_write_data_wrong_upper_limit(self):
        """
        Validates write data with (starting position + data length) > upper limit
        """
        params = self.get_parameters(starting_position=self.tde_max_size - 4,
                                     number_of_bytes=self.tde_buffer_size,
                                     write_dict=self.get_write_parameters(err_code=ErrorCodes.INVALID_ARGUMENT))
        self.process_api(params)

        self.testCaseChecked("ERR_1EB0_0002", _AUTHOR)
    # end def test_tde_write_data_wrong_upper_limit

    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_tde_write_data_wrong_length(self):
        """
        Validates write data with wrong buffer length
        """
        params = self.get_parameters(number_of_bytes=self.tde_buffer_size + 10,
                                     write_dict=self.get_write_parameters(err_code=ErrorCodes.INVALID_ARGUMENT))
        self.process_api(params)

        self.testCaseChecked("ERR_1EB0_0003", _AUTHOR)
    # end def test_tde_write_data_wrong_length

    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_tde_read_data_wrong_starting_position(self):
        """
        Validates read data with wrong start position
        """
        params = self.get_parameters(starting_position=self.tde_max_size + 1,
                                     read_dict=self.get_read_parameters(err_code=ErrorCodes.INVALID_ARGUMENT))
        self.process_api(params)

        self.testCaseChecked("ERR_1EB0_0004", _AUTHOR)
    # end def test_tde_read_data_wrong_starting_position

    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_tde_read_data_wrong_upper_limit(self):
        """
        Validates read data with (starting position + length) > upper limit
        """
        params = self.get_parameters(starting_position=self.tde_max_size - 4,
                                     number_of_bytes=self.tde_buffer_size,
                                     read_dict=self.get_read_parameters(err_code=ErrorCodes.INVALID_ARGUMENT))
        self.process_api(params)

        self.testCaseChecked("ERR_1EB0_0005", _AUTHOR)
    # end def test_tde_read_data_wrong_upper_limit

    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_tde_read_data_wrong_length(self):
        """
        Validates read data with wrong buffer length
        """
        params = self.get_parameters(number_of_bytes=self.tde_buffer_size + 10,
                                     read_dict=self.get_read_parameters(err_code=ErrorCodes.INVALID_ARGUMENT))
        self.process_api(params)

        self.testCaseChecked("ERR_1EB0_0006", _AUTHOR)
    # end def test_tde_read_data_wrong_length

    @features('Feature1EB0')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_1eb0.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetTdeMemLength request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1eb0.get_tde_mem_length_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1eb0_index)
            report.functionIndex = function_index

            TdeAccessToNvmTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1EB0_0007", _AUTHOR)
    # end def test_wrong_function_index
# end class TdeAccessToNvmErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
