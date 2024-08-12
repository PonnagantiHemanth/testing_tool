#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80d0.interface
:brief: HID++ 2.0 ``CombinedPedals`` interface test suite
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
class CombinedPedalsInterfaceTestCase(CombinedPedalsTestCase):
    """
    Validates ``CombinedPedals`` interface test cases
    """
    @features("Feature80D0")
    @level("Interface")
    def test_get_combined_pedals_interface(self):
        """
        Validate ``GetCombinedPedals`` interface
        """
        combined_pedals_enabled = False
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
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "combined_pedals_enabled": (checker.check_combined_pedals_enabled, combined_pedals_enabled),
        })
        checker.check_fields(self, response, self.feature_80d0.get_combined_pedals_response_cls, check_map)

        self.testCaseChecked("INT_80D0_0001", _AUTHOR)
    # end def test_get_combined_pedals_interface

    @features("Feature80D0")
    @level("Interface")
    def test_set_combined_pedals_interface(self):
        """
        Validate ``SetCombinedPedals`` interface
        """
        enable_combined_pedals = False
        combined_pedals_enabled = False
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetCombinedPedals request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_80d0.set_combined_pedals_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_80d0_index,
            enable_combined_pedals=enable_combined_pedals)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_80d0.set_combined_pedals_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetCombinedPedalsResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = CombinedPedalsTestUtils.CombinedPedalsResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
            "combined_pedals_enabled": (checker.check_combined_pedals_enabled, combined_pedals_enabled),
        })
        checker.check_fields(self, response, self.feature_80d0.set_combined_pedals_response_cls, check_map)

        self.testCaseChecked("INT_80D0_0002", _AUTHOR)
    # end def test_set_combined_pedals_interface
# end class CombinedPedalsInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
