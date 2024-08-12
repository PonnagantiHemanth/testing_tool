#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1004.errorhandling
:brief: HID++ 2.0 Unified Battery errorhandling test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.device.hidpp20.common.feature_1004.unifiedbattery import UnifiedBatteryGenericTest


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class UnifiedBatteryErrorHandlingTestCase(UnifiedBatteryGenericTest):
    """
    Validates Unified Battery Error Handling TestCases
    """
    @features('Feature1004')
    @level('ErrorHandling')
    def test_wrong_function_id(self):
        """
        Invalid Function index shall raise an error.

        [0] get_capabilities() -> supported_levels, flags
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over functionIndex invalid range (typical wrong values)')
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(self.feature_1004.get_max_function_index() + 1)],
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send get_capabilities request with functionIndex {function_index}')
            # ----------------------------------------------------------------------------------------------------------
            feature_1004_index, feature_1004, device_index, _ = \
                UnifiedBatteryTestUtils.HIDppHelper.get_parameters(self)
            get_capabilities_request = feature_1004.get_capabilities_cls(device_index=device_index,
                                                                         feature_index=feature_1004_index)
            get_capabilities_request.functionIndex = function_index
            get_capabilities_response = ChannelUtils.send(test_case=self,
                                                          report=get_capabilities_request,
                                                          response_queue_name=HIDDispatcher.QueueName.ERROR,
                                                          response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=int(get_capabilities_response.errorCode),
                             msg="The parameter error_code differs from the expected one")
        # end for

        self.testCaseChecked("ERR_1004_0001")
    # end def test_wrong_function_id
# end class UnifiedBatteryErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
