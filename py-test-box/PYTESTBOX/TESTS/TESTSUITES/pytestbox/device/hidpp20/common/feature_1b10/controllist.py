#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b10.controllist
:brief: Validate HID++ 2.0 ``ControlList`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2023/06/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.controllistutils import ControlListTestUtils
from pytestbox.device.base.layoututils import LayoutTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ControlListTestCase(DeviceBaseTestCase):
    """
    Validate ``ControlList`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()
        self.post_requisite_reload_us_layout = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1B10 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1b10_index, self.feature_1b10, _, _ = ControlListTestUtils.HIDppHelper.get_parameters(
            test_case=self)

        self.config = self.f.PRODUCT.FEATURES.COMMON.CONTROL_LIST
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_us_layout:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Switch back to the default Keyboard layout")
                # ------------------------------------------------------------------------------------------------------
                LayoutTestUtils.select_layout(test_case=self)
                # Refresh the cache of control id list after changed keyboard layout
                ControlListTestUtils.refresh_cid_list(test_case=self)
            # end if
        # end with

        super().tearDown()
    # end def tearDown
# end class ControlListTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
