#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4531.errorhandling
:brief: HID++ 2.0 ``MultiPlatform`` error handling test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/13
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
from pytestbox.device.base.multiplatformutils import MultiPlatformTestUtils
from pytestbox.device.hidpp20.keyboard.feature_4531.multiplatform import MultiPlatformTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiPlatformErrorHandlingTestCase(MultiPlatformTestCase):
    """
    Validate ``MultiPlatform`` errorhandling test cases
    """

    @features("Feature4531")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_4531.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetFeatureInfos request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.get_feature_infos_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index)
            report.function_index = function_index

            MultiPlatformTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_4531_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature4531")
    @level("ErrorHandling")
    def test_invalid_platform_descriptor_index(self):
        """
        Validate that an invalid platformDescriptorIndex raises an error INVALID_ARGUMENT(0x02)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over platform_descriptor_index in invalid range (i.e."
                                 "numPlatformDescr..0xFF)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_platform_descriptor_index in range(len(self.config.F_OsMask), 0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send getPlatformDescriptor request with platformDescriptorIndex ="
                                     f"{invalid_platform_descriptor_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.get_platform_descriptor_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                platform_descriptor_index=invalid_platform_descriptor_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) Error Code returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            MultiPlatformTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])

        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4531_0002", _AUTHOR)
    # end def test_invalid_platform_descriptor_index

    @features("Feature4531")
    @level("ErrorHandling")
    def test_get_host_platform_with_invalid_host_index(self):
        """
        Validate that an invalid hostIndex raises an error INVALID_ARGUMENT(0x02)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over hostIndex in invalid range (i.e. numHosts..0xFE)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts, 0xFF - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send getHostPlatform request with hostIndex = {invalid_host_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.get_host_platform_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=invalid_host_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) Error Code returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            MultiPlatformTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4531_0003", _AUTHOR)
    # end def test_get_host_platform_with_invalid_host_index

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("ErrorHandling")
    def test_set_host_platform_with_invalid_host_index(self):
        """
        Validate that an invalid hostIndex raises an error INVALID_ARGUMENT(0x02)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over hostIndex in invalid range (i.e. numHosts..0xFE)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_host_index in range(self.f.PRODUCT.DEVICE.F_NbHosts + 1, 0xFF - 1):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setHostPlatform request with hostIndex = {invalid_host_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.set_host_platform_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=invalid_host_index,
                platform_index=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) Error Code returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            MultiPlatformTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4531_0004", _AUTHOR)
    # end def test_set_host_platform_with_invalid_host_index

    @features("Feature4531")
    @features("SetHostPlatform")
    @level("ErrorHandling")
    def test_set_host_platform_with_invalid_platform_index(self):
        """
        Validate that an invalid platformIndex raises an error INVALID_ARGUMENT(0x02)
        """
        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over platform_index in invalid range (i.e. numPlatforms..0xFF)")
        # --------------------------------------------------------------------------------------------------------------
        for invalid_platform_index in range(len(self.config.F_OsMask), 0xFF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send setHostPlatform request with platformIndex= {invalid_platform_index}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_4531.set_host_platform_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_4531_index,
                host_index=0xFF,
                platform_index=invalid_platform_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check INVALID_ARGUMENT(0x02) Error Code returned by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            MultiPlatformTestUtils.HIDppHelper.send_report_wait_error(
                test_case=self,
                report=report,
                error_codes=[ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_4531_0005", _AUTHOR)
    # end def test_set_host_platform_with_invalid_platform_index

    @features("Feature4531")
    @features("NoSetHostPlatform")
    @level("ErrorHandling")
    def test_unimplemented_set_host_platform_operation(self):
        """
        Validate that an un-permitted/unimplemented operation will raises an error NOT_ALLOWED(0x05) (If the
        getFeatureInfos.capabilityMask.setHostPlatform is not supported)
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send setHostPlatform request with hostIndex = {0xFF}, platformIndex = {0}")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_4531.set_host_platform_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_4531_index,
            host_index=0xFF,
            platform_index=0x00)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check NOT_ALLOWED(0x05) Error Code returned by the DUT")
        # --------------------------------------------------------------------------------------------------------------
        MultiPlatformTestUtils.HIDppHelper.send_report_wait_error(
            test_case=self,
            report=report,
            error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_4531_0006", _AUTHOR)
    # end def test_unimplemented_set_host_platform_operation
# end class MultiPlatformErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
