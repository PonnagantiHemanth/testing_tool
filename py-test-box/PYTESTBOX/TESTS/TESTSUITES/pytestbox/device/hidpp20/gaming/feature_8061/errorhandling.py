#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.errorhandling
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hidpp20.gaming.feature_8061.extendedadjustablereportrate import \
    ExtendedAdjustableReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateErrorHandlingTestCase(ExtendedAdjustableReportRateTestCase):
    """
    Validate ``ExtendedAdjustableReportRate`` errorhandling test cases
    """

    @features("Feature8061")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over functionIndex invalid range (typical wrong values)")
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_8061.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getDeviceCapabilities request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8061.get_device_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                connection_type=0x00)
            report.functionIndex = function_index

            ExtendedAdjustableReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8061_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature8061")
    @level("ErrorHandling")
    def test_unsupported_connection_type_with_get_device_capabilities(self):
        """
        Validate that an unsupported connectionType raises an error INVALID_ARGUMENT(0x02)
        """
        # bit 0: Wired, bit 1: Gaming Wireless protocol, bit 2 to bit 7: Reserved for future usage
        unsupported_connection_type = [2**i for i in range(1, 8)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over connectionType invalid range (the device unsupported values)")
        # --------------------------------------------------------------------------------------------------------------
        for connection_type in unsupported_connection_type:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f"Send getDeviceCapabilities request with a unsupported connection type:{connection_type}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8061.get_device_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                connection_type=connection_type)

            ExtendedAdjustableReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8061_0002", _AUTHOR)
    # end def test_unsupported_connection_type_with_get_device_capabilities

    @features("Feature8061")
    @level("ErrorHandling")
    def test_unsupported_connection_type_with_get_report_rate(self):
        """
        Validate that an unsupported connectionType raises an error INVALID_ARGUMENT(0x02)
        """
        # bit 0: Wired, bit 1: Gaming Wireless protocol, bit 2 to bit 7: Reserved for future usage
        unsupported_connection_type = [2**i for i in range(1, 8)]
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test loop over connectionType invalid range (the device unsupported values)")
        # --------------------------------------------------------------------------------------------------------------
        for connection_type in unsupported_connection_type:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getReportRate request with a unsupported connection type:{connection_type}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8061.get_report_rate_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                connection_type=connection_type)

            ExtendedAdjustableReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8061_0003", _AUTHOR)
    # end def test_unsupported_connection_type_with_get_report_rate

    @features("Feature8061")
    @features("Feature8100")
    @level("ErrorHandling")
    def test_unsupported_report_rate(self):
        """
        Validate that an unsupported reportRate raises an error INVALID_ARGUMENT(0x02)
        """
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send SetOnboardMode request with onboardMode = {OnboardProfiles.Mode.HOST_MODE}")
        # ----------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self,
                                                              onboard_mode=OnboardProfiles.Mode.HOST_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over report_rate in the device unsupported value range")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in ExtendedAdjustableReportRateTestUtils.get_unsupported_report_rate(test_case=self):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setReportRate request with a unsupported report rate:{report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8061.set_report_rate_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                report_rate=report_rate)

            ExtendedAdjustableReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8061_0004", _AUTHOR)
    # end def test_unsupported_report_rate

    @features("Feature8061")
    @level("ErrorHandling")
    def test_set_report_rate_in_onboard_mode(self):
        """
        Validate that set report rate in onboard mode raises an error INVALID_ARGUMENT(0x02)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over report_rate in the device supported value range")
        # --------------------------------------------------------------------------------------------------------------
        for report_rate in ExtendedAdjustableReportRateTestUtils.get_supported_rate_list(test_case=self):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setReportRate request with a supported report rate:{report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8061.set_report_rate_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                report_rate=report_rate)

            ExtendedAdjustableReportRateTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_8061_0005", _AUTHOR)
    # end def test_set_report_rate_in_onboard_mode
# end class ExtendedAdjustableReportRateErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
