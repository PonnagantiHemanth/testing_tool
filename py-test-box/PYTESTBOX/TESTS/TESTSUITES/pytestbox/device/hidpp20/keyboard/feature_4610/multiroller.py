#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4610.multiroller
:brief: Validate HID++ 2.0 ``MultiRoller`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2023/10/03
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.multirollerutils import MultiRollerTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MultiRollerTestCase(DeviceBaseTestCase):
    """
    Validate ``MultiRoller`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x4610 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_4610_index, self.feature_4610, _, _ = MultiRollerTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.KEYBOARD.MULTI_ROLLER
    # end def setUp
# end class MultiRollerTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
