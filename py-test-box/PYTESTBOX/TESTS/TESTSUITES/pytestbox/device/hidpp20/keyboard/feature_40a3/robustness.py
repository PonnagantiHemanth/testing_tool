#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_40a3.robustness
:brief: HID++ 2.0 ``FnInversionForMultiHostDevices`` robustness test suite
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/9/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevices
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_inf_values
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.hostsinfoutils import HostsInfoTestUtils
from pytestbox.device.hidpp20.keyboard.feature_40a3.fninversionformultihostdevices \
    import FnInversionForMultiHostDevicesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"
_LOOP_END = "End Test Loop"
_LOOP_START_PADDING = "Test loop over padding range (several interesting values)"
_LOOP_START_SW_ID = "Test loop over software id range (several interesting values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesRobustnessTestCase(FnInversionForMultiHostDevicesTestCase):
    """
    Validate ``FnInversionForMultiHostDevices`` robustness test cases
    """

    @features("Feature40A3")
    @level("Robustness")
    @bugtracker("Default_Fn_Inversion_State")
    def test_get_global_fn_inversion_software_id(self):
        """
        Validate ``GetGlobalFnInversion`` software id field is ignored by the firmware

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.0xPP.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        host_index = FnInversionForMultiHostDevices.HostIndex.HOST1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(FnInversionForMultiHostDevices.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetGlobalFnInversion request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_40a3.get_global_fn_inversion_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_40a3_index,
                host_index=host_index)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_40a3.get_global_fn_inversion_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetGlobalFnInversionResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
            })
            checker.check_fields(self, response, self.feature_40a3.get_global_fn_inversion_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_40A3_0001#1", _AUTHOR)
    # end def test_get_global_fn_inversion_software_id

    @features("Feature40A3")
    @level("Robustness")
    @bugtracker("Default_Fn_Inversion_State")
    def test_set_global_fn_inversion_software_id(self):
        """
        Validate ``SetGlobalFnInversion`` software id field is ignored by the firmware

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.FnInversionState.0xPP

        SwID boundary values [1..F] (0 is not allowed since event is present)
        """
        host_index = FnInversionForMultiHostDevices.HostIndex.HOST1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_SW_ID)
        # --------------------------------------------------------------------------------------------------------------
        for software_id in compute_inf_values(FnInversionForMultiHostDevices.DEFAULT.SOFTWARE_ID)[1:]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGlobalFnInversion request with software_id: {software_id}")
            # ----------------------------------------------------------------------------------------------------------
            report = self.feature_40a3.set_global_fn_inversion_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_40a3_index,
                host_index=host_index,
                fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)
            report.softwareId = software_id
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_40a3.set_global_fn_inversion_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetGlobalFnInversionResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FnInversionForMultiHostDevicesTestUtils.SetGlobalFnInversionResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "fn_inversion_state": (checker.check_fn_inversion_state,
                                       FnInversionForMultiHostDevices.FnInversionState.ON),
            })
            checker.check_fields(self, response, self.feature_40a3.set_global_fn_inversion_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_40A3_0001#2", _AUTHOR)
    # end def test_set_global_fn_inversion_software_id

    @features("Feature40A3")
    @level("Robustness")
    @bugtracker("Default_Fn_Inversion_State")
    def test_get_global_fn_inversion_padding(self):
        """
        Validate ``GetGlobalFnInversion`` padding bytes are ignored by the firmware

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.0xPP.0xPP

        Padding (PP) boundary values [00..FF]
        """
        host_index = FnInversionForMultiHostDevices.HostIndex.HOST1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_40a3.get_global_fn_inversion_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetGlobalFnInversion request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_40a3_index,
                host_index=host_index)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_40a3.get_global_fn_inversion_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetGlobalFnInversionResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
            })
            checker.check_fields(self, response, self.feature_40a3.get_global_fn_inversion_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_40A3_0002#1", _AUTHOR)
    # end def test_get_global_fn_inversion_padding

    @features("Feature40A3")
    @level("Robustness")
    @bugtracker("Default_Fn_Inversion_State")
    def test_set_global_fn_inversion_padding(self):
        """
        Validate ``SetGlobalFnInversion`` padding bytes are ignored by the firmware

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477

        Request: 0x10.DeviceIndex.FeatureIndex.FunctionIndex|SwID.HostIndex.FnInversionState.0xPP

        Padding (PP) boundary values [00..FF]
        """
        host_index = FnInversionForMultiHostDevices.HostIndex.HOST1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_PADDING)
        # --------------------------------------------------------------------------------------------------------------
        request_cls = self.feature_40a3.set_global_fn_inversion_cls
        for padding in compute_sup_values(HexList(Numeral(request_cls.DEFAULT.PADDING, request_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetGlobalFnInversion request with padding: {padding}")
            # ----------------------------------------------------------------------------------------------------------
            report = request_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_40a3_index,
                host_index=host_index,
                fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)
            report.padding = padding
            response = ChannelUtils.send(
                test_case=self,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=self.feature_40a3.set_global_fn_inversion_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SetGlobalFnInversionResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = FnInversionForMultiHostDevicesTestUtils.SetGlobalFnInversionResponseChecker
            check_map = checker.get_default_check_map(self)
            check_map.update({
                "host_index": (checker.check_host_index, host_index),
                "fn_inversion_state": (checker.check_fn_inversion_state,
                                       FnInversionForMultiHostDevices.FnInversionState.ON),
            })
            checker.check_fields(self, response, self.feature_40a3.set_global_fn_inversion_response_cls, check_map)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_40A3_0002#2", _AUTHOR)
    # end def test_set_global_fn_inversion_padding
# end class FnInversionForMultiHostDevicesRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
