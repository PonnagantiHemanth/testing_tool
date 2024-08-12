#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pytestbox.device.hidpp20.common.feature_1E01_robustness
    :brief: HID++ 2.0 Manage deactivatable features robustness test suite
    :author: Martin Cryonnet
    :date: 2020/10/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.device.base.managedeactivatablefeaturesutils import ManageDeactivatableFeaturesTestUtils
from pytestbox.device.hidpp20.common.feature_1E01 import ManageDeactivatableFeaturesTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ManageDeactivatableFeaturesRobustnessTestCase(ManageDeactivatableFeaturesTestCase):
    """
    Validates Manage deactivatable features robustness TestCases in Application mode
    """
    @features('Feature1E01')
    @features('Feature1E01WithManufacturingCounter')
    @level('Robustness')
    def test_set_counter_out_of_range_manuf_hidpp(self):
        """
        Check setCounters is working when sending a manufacturing counter value greater than the product specific
        maximum allowable value
        """
        max_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter
        out_of_range_values = compute_sup_values(max_counter)
        assert 0xFF in out_of_range_values
        expected_values = [max_counter] * len(out_of_range_values)
        self._test_set_counter_range(values_range=out_of_range_values, expected_manuf_hidpp_range=expected_values)
        self.testCaseChecked("ROT_1E01_0004#1")
    # end def test_set_counter_out_of_range_manuf_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithComplianceCounter')
    @level('Robustness')
    def test_set_counter_out_of_range_compl_hidpp(self):
        """
        Check setCounters is working when sending a compliance counter value greater than the product specific
        maximum allowable value
        """
        max_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter
        out_of_range_values = compute_sup_values(max_counter)
        assert 0xFF in out_of_range_values
        expected_values = [max_counter] * len(out_of_range_values)
        self._test_set_counter_range(values_range=out_of_range_values, expected_compl_hidpp_range=expected_values)
        self.testCaseChecked("ROT_1E01_0004#2")
    # end def test_set_counter_out_of_range_compl_hidpp

    @features('Feature1E01')
    @features('Feature1E01WithGothardCounter')
    @level('Robustness')
    def test_set_counter_out_of_range_gothard(self):
        """
        Check setCounters is working when sending a Gothard counter value greater than the product specific
        maximum allowable value
        """
        max_counter = self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter
        out_of_range_values = compute_sup_values(max_counter)
        expected_values = [max_counter] * len(out_of_range_values)
        self._test_set_counter_range(values_range=out_of_range_values, expected_manuf_hidpp_range=expected_values)
        self.testCaseChecked("ROT_1E01_0004#3")
    # end def test_set_counter_out_of_range_gothard

    @features('Feature1E01')
    @level('Robustness')
    def test_set_counter_padding_ignored(self):
        """
        Padding bytes shall be ignored by the firmware
        """
        for padding in compute_sup_values(HexList(Numeral(self.feature_1e01.set_counters_cls.DEFAULT.PADDING,
                                                        self.feature_1e01.set_counters_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send SetCounters request default values with padding not to default value')
            # ----------------------------------------------------------------------------
            set_counters_req = self.feature_1e01.set_counters_cls(
             self.deviceIndex,
             self.feature_1e01_index,
             gothard=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportGothardCounter,
             compl_hidpp=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportComplianceCounter,
             manuf_hidpp=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_SupportManufacturingCounter,
             manuf_hidpp_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter,
             compl_hidpp_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter,
             gothard_counter=self.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter
            )
            set_counters_req.padding = padding

            set_counters_resp = self.send_report_wait_response(
                report=set_counters_req,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_1e01.set_counters_response_cls)

            # ----------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check SetCounters response fields')
            # ----------------------------------------------------------------------------
            ManageDeactivatableFeaturesTestUtils.MessageChecker.check_fields(
                self, set_counters_resp, self.feature_1e01.set_counters_response_cls, {})
        # end for
        self.testCaseChecked("ROT_1E01_0006")
    # end def test_set_counter_padding_ignored
# end class ManageDeactivatableFeaturesRobustnessTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
