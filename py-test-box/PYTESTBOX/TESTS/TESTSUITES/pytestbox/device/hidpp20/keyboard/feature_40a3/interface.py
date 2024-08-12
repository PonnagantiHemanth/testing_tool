#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_40a3.interface
:brief: HID++ 2.0 ``FnInversionForMultiHostDevices`` interface test suite
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
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.hidpp20.keyboard.feature_40a3.fninversionformultihostdevices \
    import FnInversionForMultiHostDevicesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Masan Xu"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevicesInterfaceTestCase(FnInversionForMultiHostDevicesTestCase):
    """
    Validate ``FnInversionForMultiHostDevices`` interface test cases
    """

    @features("Feature40A3")
    @level("Interface")
    @bugtracker("Default_Fn_Inversion_State")
    def test_get_global_fn_inversion(self):
        """
        Validate ``GetGlobalFnInversion`` interface

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477
        """
        host_index = FnInversionForMultiHostDevices.HostIndex.HOST1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetGlobalFnInversion request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_40a3.get_global_fn_inversion_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_40a3_index,
            host_index=host_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_40a3.get_global_fn_inversion_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetGlobalFnInversionResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FnInversionForMultiHostDevicesTestUtils.GetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "host_index": (checker.check_host_index, host_index),
        })
        checker.check_fields(self, response, self.feature_40a3.get_global_fn_inversion_response_cls, check_map)

        self.testCaseChecked("INT_40A3_0001", _AUTHOR)
    # end def test_get_global_fn_inversion

    @features("Feature40A3")
    @level("Interface")
    @bugtracker("Default_Fn_Inversion_State")
    def test_set_global_fn_inversion(self):
        """
        Validate ``SetGlobalFnInversion`` interface

        Related to Jira ticket: https://jira.logitech.io/browse/NRF52-477
        """
        host_index = FnInversionForMultiHostDevices.HostIndex.HOST1
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetGlobalFnInversion request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_40a3.set_global_fn_inversion_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_40a3_index,
            host_index=host_index,
            fn_inversion_state=FnInversionForMultiHostDevices.FnInversionState.ON)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
            response_class_type=self.feature_40a3.set_global_fn_inversion_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetGlobalFnInversionResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = FnInversionForMultiHostDevicesTestUtils.SetGlobalFnInversionResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "host_index": (checker.check_host_index, host_index),
            "fn_inversion_state": (checker.check_fn_inversion_state,
                                   FnInversionForMultiHostDevices.FnInversionState.ON),
        })
        checker.check_fields(self, response, self.feature_40a3.set_global_fn_inversion_response_cls, check_map)

        self.testCaseChecked("INT_40A3_0002", _AUTHOR)
    # end def test_set_global_fn_inversion
# end class FnInversionForMultiHostDevicesInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
