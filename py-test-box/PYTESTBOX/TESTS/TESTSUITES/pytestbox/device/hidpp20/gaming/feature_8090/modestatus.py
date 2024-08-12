#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.gaming.feature_8090.modestatus
:brief: Validate HID++ 2.0 ``ModeStatus`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2022/08/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.modestatusutils import ModeStatusTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ModeStatusTestCase(DeviceBaseTestCase):
    """
    Validate ``ModeStatus`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8090 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8090_index, self.feature_8090, _, _ = ModeStatusTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.MODE_STATUS
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class ModeStatusTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
