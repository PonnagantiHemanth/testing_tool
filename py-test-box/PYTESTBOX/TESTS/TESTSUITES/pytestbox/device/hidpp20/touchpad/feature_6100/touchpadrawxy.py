#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.touchpad.feature_6100.touchpadrawxy
:brief: Validate HID++ 2.0 ``TouchpadRawXY`` feature
:author: Masan Xu <mxu11@logitech.com>
:date: 2022/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.touchpadrawxyutils import TouchpadRawXYTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TouchpadRawXYTestCase(DeviceBaseTestCase):
    """
    Validate ``TouchpadRawXY`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x6100 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_6100_index, self.feature_6100, _, _ = TouchpadRawXYTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.TOUCHPAD.TOUCHPAD_RAW_XY
    # end def setUp
# end class TouchpadRawXYTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
