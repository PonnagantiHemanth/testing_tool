#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.gaming.feature_8061.extendedadjustablereportrate
:brief: Validate HID++ 2.0 ``ExtendedAdjustableReportRate`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2022/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ExtendedAdjustableReportRateTestCase(DeviceBaseTestCase):
    """
    Validate ``ExtendedAdjustableReportRate`` TestCases in Application mode
    """

    def setUp(self):
        """
        Handle test prerequisites
        """
        self.post_requisite_unpluging_usb_cable = False
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8061 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_8061_index, self.feature_8061, _, _ = \
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(self)

        self.config = self.f.PRODUCT.FEATURES.GAMING.EXTENDED_ADJUSTABLE_REPORT_RATE
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites
        """
        with self.manage_post_requisite():
            if self.post_requisite_unpluging_usb_cable:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Power OFF the USB cable and switch to the receiver channel')
                # ------------------------------------------------------------------------------------------------------
                ProtocolManagerUtils.exit_usb_channel(test_case=self)
            # end if
        # end with
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
# end class ExtendedAdjustableReportRateTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
