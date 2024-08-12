#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_8135.interface
:brief: HID++ 2.0 ``PedalStatus`` interface test suite
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/04/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.pedalstatusutils import PedalStatusTestUtils
from pytestbox.device.hidpp20.gaming.feature_8135.pedalstatus import PedalStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Vasudev Mukkamala"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PedalStatusInterfaceTestCase(PedalStatusTestCase):
    """
    Validate ``PedalStatus`` interface test cases
    """

    @features("Feature8135")
    @level("Interface")
    def test_get_pedal_status_interface(self):
        """
        Validate ``GetPedalStatus`` interface
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetPedalStatus request")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_8135.get_pedal_status_cls(
            device_index=self.deviceIndex,
            feature_index=self.feature_8135_index)
        response = self.send_report_wait_response(
            report=report,
            response_queue=self.hidDispatcher.gaming_message_queue,
            response_class_type=self.feature_8135.get_pedal_status_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check GetPedalStatusResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = PedalStatusTestUtils.GetPedalStatusResponseChecker
        check_map = checker.get_default_check_map(self)
        check_map.update({
            "deviceIndex": (checker.check_device_index, report.deviceIndex),
            "featureIndex": (checker.check_feature_index, report.featureIndex),
        })
        checker.check_fields(self, response, self.feature_8135.get_pedal_status_response_cls, check_map)

        self.testCaseChecked("INT_8135_0001", _AUTHOR)
    # end def test_get_pedal_status_interface
# end class PedalStatusInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
