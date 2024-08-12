#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_18a1.ledtest
:brief: Validate HID++ 2.0 ``LEDTest`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.ledtestutils import LEDTestTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class LEDTestTestCase(DeviceBaseTestCase):
    """
    Validate ``LEDTest`` TestCases in Application mode
    """

    # noinspection PyAttributeOutsideInit
    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Activate features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x18A1 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_18a1_index, self.feature_18a1, _, _ = LEDTestTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.LED_TEST
    # end def setUp
# end class LEDTestTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
