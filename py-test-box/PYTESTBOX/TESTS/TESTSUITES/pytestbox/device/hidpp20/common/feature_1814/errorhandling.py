#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1814.errorhandling
:brief: HID++ 2.0 ``ChangeHost`` error handling test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.changehostutils import ChangeHostTestUtils
from pytestbox.device.hidpp20.common.feature_1814.changehost import ChangeHostTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Kevin Dayet"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ChangeHostErrorHandlingTestCase(ChangeHostTestCase):
    """
    Validate ``ChangeHost`` errorhandling test cases
    """

    @features("Feature1814")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index

        Function indexes valid range [0..3],
        Tests wrong indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_1814.get_max_function_index() + 1)),
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetHostInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_1814.get_host_info_cls(
                ChannelUtils.get_device_index(test_case=self), self.feature_1814_index)
            report.functionIndex = function_index

            ChangeHostTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1814_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features('Feature1814')
    @level('ErrorHandling')
    def test_set_host_wrong_host_index(self):
        """
        Validates ``SetCurrentHost`` with invalid hostIndex

        Host indexes valid range [0..nbHost-1],
        Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Test Loop over hostIndex invalid range ([{self.f.PRODUCT.DEVICE.F_NbHosts + 1}..0xFF])")
        # ---------------------------------------------------------------------------
        for index in compute_sup_values(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCurrentHost with wrong index value={index}")
            # ---------------------------------------------------------------------------
            report = self.feature_1814.set_current_host_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=index)
            ChangeHostTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ERR_1814_0002", _AUTHOR)
    # end def test_set_host_wrong_host_index

    @features('Feature1814')
    @level('ErrorHandling')
    def test_set_cookie_wrong_host_index(self):
        """
        Validates SetCookie with invalid hostIndex

        Host indexes valid range [0..nbHost-1],
            Tests wrong indexes
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(
            self, f"Test Loop over hostIndex invalid range ([{self.f.PRODUCT.DEVICE.F_NbHosts + 1}..0xFF])")
        # ---------------------------------------------------------------------------
        for index in compute_sup_values(self.f.PRODUCT.DEVICE.F_NbHosts):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetCookie with wrong index value={index}")
            # ---------------------------------------------------------------------------
            report = self.feature_1814.set_cookie_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_1814_index,
                host_index=index,
                cookie=0)
            ChangeHostTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ERR_1814_0003", _AUTHOR)
    # end def test_set_cookie_wrong_host_index
# end class ChangeHostErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
