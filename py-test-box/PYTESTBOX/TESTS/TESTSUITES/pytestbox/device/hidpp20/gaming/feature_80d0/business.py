#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80d0.business
:brief: HID++ 2.0 ``CombinedPedals`` business test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.combinedpedalsutils import CombinedPedalsTestUtils
from pytestbox.device.hidpp20.gaming.feature_80d0.combinedpedals import CombinedPedalsTestCase


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CombinedPedalsBusinessTestCase(CombinedPedalsTestCase):
    """
    Validates ``CombinedPedals`` business test cases
    """
    @features("Feature80D0")
    @level("Business")
    def test_combined_pedals_business(self):
        """
        Validate ``GetCombinedPedals`` business test
        """
        combined_pedals_enabled = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        CombinedPedalsTestUtils.HIDppHelper.set_combined_pedals(self, enable_combined_pedals=combined_pedals_enabled)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80d0.get_combined_pedals_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_80d0_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_80d0.get_combined_pedals_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetCombinedPedalsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
        checker.check_fields(self, response, self.feature_80d0.get_combined_pedals_response_cls)

        self.testCaseChecked("BUS_80D0_0001", _AUTHOR)
    # end def test_combined_pedals_business
# end class CombinedPedalsBusinessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
