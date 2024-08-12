#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.interface
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` interface test suite
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.hexlist import HexList
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
class ExtendedAdjustableReportRateInterfaceTestCase(ExtendedAdjustableReportRateTestCase):
    """
    Validate ``ExtendedAdjustableReportRate`` interface test cases
    """

    @features("Feature8061")
    @level("Interface")
    def test_get_device_capabilities_interface(self):
        """
        Validate ``GetDeviceCapabilities`` interface
        """
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetDeviceCapabilities request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8061.get_device_capabilities_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_8061_index,
            connection_type=HexList(connection_type))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8061.get_device_capabilities_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetDeviceCapabilitiesResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ExtendedAdjustableReportRateTestUtils.GetDeviceCapabilitiesResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_8061.get_device_capabilities_response_cls, check_map)

        self.testCaseChecked("INT_8061_0001", _AUTHOR)
    # end def test_get_device_capabilities_interface

    @features("Feature8061")
    @level("Interface")
    def test_get_actual_report_rate_list_interface(self):
        """
        Validate ``GetActualReportRateList`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetActualReportRateList request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8061.get_actual_report_rate_list_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_8061_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8061.get_actual_report_rate_list_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetActualReportRateListResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ExtendedAdjustableReportRateTestUtils.GetActualReportRateListResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_8061.get_actual_report_rate_list_response_cls, check_map)

        self.testCaseChecked("INT_8061_0002", _AUTHOR)
    # end def test_get_actual_report_rate_list_interface

    @features("Feature8061")
    @level("Interface")
    def test_get_report_rate_interface(self):
        """
        Validate ``GetReportRate`` interface
        """
        connection_type = ExtendedAdjustableReportRateTestUtils.get_current_connection_type_index(self)
        # Handle both wired and wireless cases
        if connection_type == ExtendedAdjustableReportRate.ConnectionType.WIRED:
            report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRateWired[0])
        elif connection_type == ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS:
            report_rate = int(self.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.OOB_PROFILES.F_ReportRateWireless[0])
        else:
            raise ValueError("Unknown Connection Type")
        # end if

        # If default report rate is not supported by current receiver, then select highest report rate
        if isinstance(self.current_channel, ThroughReceiverChannel):
            report_rate_list = HexList(self.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
                                       .F_SupportedReportRateList[connection_type])
            channel_rate_list = HexList(ExtendedAdjustableReportRateTestUtils.get_channel_report_rate_list(
                self.current_channel.receiver_channel))
            report_rate_list &= channel_rate_list
            if not report_rate_list.testBit(report_rate):
                report_rate = ExtendedAdjustableReportRateTestUtils.get_highest_report_rate(self)
            # end if
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetReportRate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8061.get_report_rate_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_8061_index,
            connection_type=connection_type)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8061.get_report_rate_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetReportRateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ExtendedAdjustableReportRateTestUtils.GetReportRateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "report_rate": (checker.check_report_rate, report_rate),
        })
        checker.check_fields(self, response, self.feature_8061.get_report_rate_response_cls, check_map)

        self.testCaseChecked("INT_8061_0003", _AUTHOR)
    # end def test_get_report_rate_interface

    @features("Feature8061")
    @features("Feature8100")
    @level("Interface")
    def test_set_report_rate_interface(self):
        """
        Validate ``SetReportRate`` interface
        """
        report_rate = HexList(0x0)
        onboard_mode = OnboardProfiles.Mode.HOST_MODE
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = {onboard_mode} (Host Mode)")
        # --------------------------------------------------------------------------------------------------------------
        OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case=self, onboard_mode=onboard_mode)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetReportRate request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8061.set_report_rate_cls(
            device_index=ChannelUtils.get_device_index(self),
            feature_index=self.feature_8061_index,
            report_rate=HexList(report_rate))
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.GAMING,
            response_class_type=self.feature_8061.set_report_rate_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetReportRateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = ExtendedAdjustableReportRateTestUtils.SetReportRateResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_8061.set_report_rate_response_cls)

        self.testCaseChecked("INT_8061_0004", _AUTHOR)
    # end def test_set_report_rate_interface
# end class ExtendedAdjustableReportRateInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
