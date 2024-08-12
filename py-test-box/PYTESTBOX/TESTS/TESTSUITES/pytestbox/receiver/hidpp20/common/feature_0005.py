#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.hidpp20.common.feature_0005
:brief: Validate Receiver HID++ 2.0 Common feature 0x0005
:author: Stanislas Cottard
:date: 2019/11/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pytestbox.base.bootloadertest import ReceiverBootloaderTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.hidpp20.common.feature_0005 import SharedDeviceTypeAndNameTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceTypeAndNameTestCase(SharedDeviceTypeAndNameTestCase, ReceiverBootloaderTestCase):
    """
    Validate Device type and name TestCases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x0005)')
        # ---------------------------------------------------------------------------
        self.feature_0005_index, self.feature_0005, _, _ = DeviceTypeAndNameTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp

# end class DeviceTypeAndNameTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
