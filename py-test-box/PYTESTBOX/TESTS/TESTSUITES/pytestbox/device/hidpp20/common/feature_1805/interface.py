#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1805.interface
:brief: HID++ 2.0 ``OobState`` interface test suite
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.tools.hexlist import HexList
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.oobstateutils import OobStateTestUtils
from pytestbox.device.hidpp20.common.feature_1805.oobstate import OobStateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Sanjib Hazra"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateInterfaceTestCase(OobStateTestCase):
    """
    Validate ``OobState`` interface test cases
    """

    @features("Feature1805")
    @level("Interface")
    @services("Debugger")
    def test_set_oob_state_interface(self):
        """
        Validate ``SetOobState`` interface
        """
        self.post_requisite_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetOobState request")
        # --------------------------------------------------------------------------------------------------------------
        response = OobStateTestUtils.HIDppHelper.set_oob_state(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check SetOobStateResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        checker = DeviceTestUtils.MessageChecker
        check_map = {
            "deviceIndex": (checker.check_device_index, HexList(ChannelUtils.get_device_index(self))),
            "featureIndex": (checker.check_feature_index, HexList(self.feature_1805_index)),
        }
        checker.check_fields(self, response, self.feature_1805.set_oob_state_response_cls, check_map)

        self.testCaseChecked("INT_1805_0001", _AUTHOR)
    # end def test_set_oob_state_interface
# end class OobStateInterfaceTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
