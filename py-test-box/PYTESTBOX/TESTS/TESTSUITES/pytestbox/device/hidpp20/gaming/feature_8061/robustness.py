#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.robustness
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` robustness test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.hidpp20.gaming.feature_8061.extendedadjustablereportrate import \
    ExtendedAdjustableReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "YY Liu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateRobustnessTestCase(ExtendedAdjustableReportRateTestCase):
    """
    Validate ``ExtendedAdjustableReportRate`` robustness test cases
    """

    @features("Feature8061")
    @level("Robustness")
    def test_get_device_capabilities_software_id(self):
        """
        Validate ``GetDeviceCapabilities`` software id field is ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ConnectionType.0xPP.0xPP

        SwID boundary values [0..F]
        """
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(ExtendedAdjustableReportRate.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDeviceCapabilities request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_8061.get_device_capabilities_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                connection_type=connection_type)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8061.get_device_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDeviceCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetDeviceCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8061.get_device_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8061_0001", _AUTHOR)
    # end def test_get_device_capabilities_software_id

    @features("Feature8061")
    @level("Robustness")
    def test_get_device_capabilities_padding(self):
        """
        Validate ``GetDeviceCapabilities`` padding bytes are ignored by the firmware

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.ConnectionType.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_8061.get_device_capabilities_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetDeviceCapabilities request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_8061_index,
                connection_type=connection_type)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=self.feature_8061.get_device_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetDeviceCapabilitiesResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.GetDeviceCapabilitiesResponseChecker
            check_map = checker.get_default_check_map(self)
            checker.check_fields(self, response, self.feature_8061.get_device_capabilities_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_8061_0002", _AUTHOR)
    # end def test_get_device_capabilities_padding
# end class ExtendedAdjustableReportRateRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
