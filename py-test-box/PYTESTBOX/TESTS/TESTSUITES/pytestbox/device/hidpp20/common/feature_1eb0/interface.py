#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1eb0.interface
:brief: HID++ 2.0 ``TdeAccessToNvm`` interface test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/07
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.tdeaccesstonvmutils import TdeAccessToNvmTestUtils
from pytestbox.device.hidpp20.common.feature_1eb0.tdeaccesstonvm import TdeAccessToNvmTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmInterfaceTestCase(TdeAccessToNvmTestCase):
    """
    Validate ``TdeAccessToNvm`` interface test cases
    """

    @features("Feature1EB0")
    @level("Interface")
    def test_get_tde_mem_length(self):
        """
        Validate ``GetTdeMemLength`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send GetTdeMemLength request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1eb0.get_tde_mem_length_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1eb0_index)
        response = ChannelUtils.send(
            test_case=self,
            report=report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1eb0.get_tde_mem_length_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetTdeMemLengthResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = TdeAccessToNvmTestUtils.GetTdeMemLengthResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_1eb0.get_tde_mem_length_response_cls, check_map)

        self.testCaseChecked("INT_1EB0_0001", _AUTHOR)
    # end def test_get_tde_mem_length

    @features("Feature1EB0")
    @level("Interface")
    def test_tde_write_data_tde_read_data(self):
        """
        Validate TdeWriteData and TdeReadData interface
        """
        params = self.get_parameters(read_dict=self.get_read_parameters(),
                                     write_dict=self.get_write_parameters())
        self.process_api(params)

        self.testCaseChecked("INT_1EB0_0002", _AUTHOR)
        self.testCaseChecked("INT_1EB0_0003", _AUTHOR)
    # end def test_tde_write_data_tde_read_data

    @features("Feature1EB0")
    @level("Interface")
    def test_tde_clear_data(self):
        """
        Validate ``TdeClearData`` interface
        """
        params = self.get_parameters(read_dict=self.get_read_parameters(err_code=ErrorCodes.HW_ERROR))
        params["clear_api"] = True
        self.process_api(params)

        self.testCaseChecked("INT_1EB0_0004", _AUTHOR)
    # end def test_tde_clear_data
# end class TdeAccessToNvmInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
