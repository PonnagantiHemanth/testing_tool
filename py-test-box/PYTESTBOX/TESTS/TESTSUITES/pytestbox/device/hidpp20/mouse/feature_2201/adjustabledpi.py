#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.mouse.feature_2201.adjustabledpi
:brief: HID++ 2.0 Adjustable DPI test case
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.adjustabledpiutils import AdjustableDpiTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AdjustableDpiTestCase(DeviceBaseTestCase):
    """
    Validates Adjustable DPI TestCases
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_reload_nvs = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 0x2201 index')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_2201_index, self.feature_2201, _, _ = AdjustableDpiTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        if self.debugger:
            DeviceTestUtils.NvsHelper.backup_nvs(self)
        # end if

        self.max_supported_dpi_levels = int(self.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_MaxSupportedDpiLevels)
        self.current_supported_dpi_levels = len(AdjustableDpiTestUtils.get_predefined_dpi_levels(self))
        self.default_dpi_level_index = AdjustableDpiTestUtils.get_default_dpi_level_index(self)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                if self.debugger:
                    DeviceTestUtils.NvsHelper.restore_nvs(self)
                # end if
                self.post_requisite_reload_nvs = False
            # end if
        # end with
        super().tearDown()
    # end def tearDown
# end class AdjustableDpiTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
