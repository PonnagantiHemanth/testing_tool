#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.gaming.feature_80d0.combinedpedals
:brief: Validate HID++ 2.0 ``CombinedPedals`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.combinedpedalsutils import CombinedPedalsTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CombinedPedalsTestCase(DeviceBaseTestCase):
    """
    Validates ``CombinedPedals`` TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x80D0 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_80d0_index, self.feature_80d0, _, _ = CombinedPedalsTestUtils.HIDppHelper.get_parameters(self)
    # end def setUp
# end class CombinedPedalsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
