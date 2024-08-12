#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.robustness
:brief: HID++ 2.0 Unified Battery robustness test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGenericTest


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UnifiedBatteryRobustnessTestCase(UnifiedBatteryGenericTest):
    """
    Validates Unified Battery Robustness TestCases
    """
    @features('Feature1004')
    @level('Robustness')
    def test_software_id_ignored(self):
        """
        SoftwareId input is ignored by the firmware

        [0] get_capabilities() -> supported_levels, flags
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over functionIndex invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_wrong_range(0, max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send get_capabilities request with softwareId = {software_id}')
            # ----------------------------------------------------------------------------------------------------------
            feature_1004_index, feature_1004, device_index, _ = \
                UnifiedBatteryTestUtils.HIDppHelper.get_parameters(self)
            get_capabilities_request = feature_1004.get_capabilities_cls(device_index=device_index,
                                                                         feature_index=feature_1004_index)
            get_capabilities_request.softwareId = software_id
            get_capabilities_response = ChannelUtils.send(
                                                    test_case=self,
                                                    report=get_capabilities_request,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=feature_1004.get_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
                test_case=self, message=get_capabilities_response,
                expected_cls=self.feature_1004.get_capabilities_response_cls)
        # end for

        self.testCaseChecked("ROB_1004_0001")
    # end def test_software_id_ignored

    @features('Feature1004')
    @level('Robustness')
    def test_padding_ignored(self):
        """
        Padding bytes shall be ignored by the firmware

        [0] get_capabilities() -> supported_levels, flags
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over functionIndex invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for padding_byte in \
                compute_sup_values(HexList(Numeral(UnifiedBattery.DEFAULT.PADDING,
                                   UnifiedBatteryTestUtils.get_padding_size_for_get_capabilities(self)))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send get_capabilities request with softwareId = {padding_byte}')
            # ----------------------------------------------------------------------------------------------------------
            feature_1004_index, feature_1004, device_index, _ = \
                UnifiedBatteryTestUtils.HIDppHelper.get_parameters(self)
            get_capabilities_request = feature_1004.get_capabilities_cls(device_index=device_index,
                                                                         feature_index=feature_1004_index)
            get_capabilities_request.padding = padding_byte
            get_capabilities_response = ChannelUtils.send(
                                                    test_case=self,
                                                    report=get_capabilities_request,
                                                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                                                    response_class_type=feature_1004.get_capabilities_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for get_capabilities response and check product-specific constants')
            # ----------------------------------------------------------------------------------------------------------
            UnifiedBatteryTestUtils.GetCapabilitiesResponseChecker.check_fields(
                test_case=self, message=get_capabilities_response,
                expected_cls=self.feature_1004.get_capabilities_response_cls)
        # end for

        self.testCaseChecked("ROB_1004_0002")
    # end def test_padding_ignored

    @features('Feature1004v1+')
    @features('NoFeature1004ShowBatteryStatusCapability')
    @level('Robustness')
    @bugtracker('Foster_ShowBatteryStatus_NotAllowed')
    def test_show_battery_status_not_supported(self):
        """
        ShowBatteryStatus shall return error NOT_ALLOWED if this command is not supported
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send show_battery_status request')
        # --------------------------------------------------------------------------------------------------------------
        show_battery_status = self.feature_1004.show_battery_status_cls(device_index=self.deviceIndex,
                                                                        feature_index=self.feature_1004_index)

        err_resp = ChannelUtils.send(
                        test_case=self,
                        report=show_battery_status,
                        response_queue_name=HIDDispatcher.QueueName.ERROR,
                        response_class_type=Hidpp2ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp20_error_message(
            test_case=self,
            error_message=err_resp,
            feature_index=show_battery_status.featureIndex,
            function_index=show_battery_status.functionIndex,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ROB_1004_0003")
    # end def test_show_battery_status_not_supported
# end class UnifiedBatteryRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
