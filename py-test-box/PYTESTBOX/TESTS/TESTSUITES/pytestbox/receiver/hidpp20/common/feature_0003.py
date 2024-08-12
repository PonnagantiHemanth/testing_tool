#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp20.common.feature_0003
:brief: Validates Receiver HID++ 2.0 Common feature 0x0003
:author: Stanislas Cottard
:date: 2019/11/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.hidpp20.common.feature_0003 import SharedDeviceInformationTestCase
from pytestbox.base.bootloadertest import ReceiverBootloaderTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceInformationTestCase(SharedDeviceInformationTestCase, ReceiverBootloaderTestCase):
    """
    Validate Device information TestCases
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp

# end class DeviceInformationTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
