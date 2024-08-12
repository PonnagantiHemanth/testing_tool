#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.peripheral.feature_9001.pmw3816andpmw3826
:brief: Validate HID++ 2.0 ``PMW3816andPMW3826`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/01/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.pmw3816andpmw3826utils import PMW3816andPMW3826TestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826TestCase(DeviceBaseTestCase):
    """
    Validate ``PMW3816andPMW3826`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Enable manufacturing features")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x9001 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_9001_index, self.feature_9001, _, _ = PMW3816andPMW3826TestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.PERIPHERAL.PMW3816_AND_PMW3826
    # end def setUp
# end class PMW3816andPMW3826TestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
