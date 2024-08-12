#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1602.passwordauthentication
:brief: Validate HID++ 2.0 ``PasswordAuthentication`` feature
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.passwordauthenticationutils import DevicePasswordAuthenticationTestUtils
from pytestbox.shared.hidpp.passwordauthentication.passwordauthentication import SharedPasswordAuthenticationTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class DevicePasswordAuthenticationTestCase(SharedPasswordAuthenticationTestCase, DeviceBaseTestCase):
    """
    Validate ``PasswordAuthentication`` TestCases in Application mode with a device as DUT
    """
    ManageUtils = DeviceManageDeactivatableFeaturesAuthTestUtils
    PasswordAuthenticationTestUtils = DevicePasswordAuthenticationTestUtils

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
        LogHelper.log_prerequisite(self, "Get feature 0x1602 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1602_index, self.feature_1602, _, _ = \
            DevicePasswordAuthenticationTestUtils.HIDppHelper.get_parameters(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x1E02 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1e02_index, self.feature_1e02, _, _ = \
            DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.get_parameters(self)
    # end def setUp
# end class DevicePasswordAuthenticationTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
