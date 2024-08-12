#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0005
:brief: Validate Device HID++ 2.0 Common feature 0x0005
https://docs.google.com/spreadsheets/d/1rYgsHRRwjKoZ7uPTFVPJ3tHp9n3QUvifbXEWTxGu7sw/edit?usp=sharing
:author: Christophe Roquebert
:date: 2018/12/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.bootloadertest import DeviceBootloaderTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.devicetypeandnameutils import DeviceTypeAndNameTestUtils
from pytestbox.shared.hidpp20.common.feature_0005 import DeviceTypeAndNameTestCaseMixin
from pytestbox.shared.hidpp20.common.feature_0005 import SharedDeviceTypeAndNameTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationDeviceTypeAndNameTestCase(SharedDeviceTypeAndNameTestCase, DeviceBaseTestCase):
    """
    Validates Device type and name TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text='Send Root.GetFeature(0x0005)')
        # ---------------------------------------------------------------------------
        self.feature_0005_index, self.feature_0005, _, _ = DeviceTypeAndNameTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp
# end class ApplicationDeviceTypeAndNameTestCase


@features.class_decorator("BootloaderAvailable", inheritance=SharedDeviceTypeAndNameTestCase)
class BootloaderDeviceTypeAndNameTestCase(SharedDeviceTypeAndNameTestCase, DeviceBootloaderTestCase):
    """
    Validates Device type and name TestCases in Bootloader mode
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        super().setUp()

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text='Send Root.GetFeature(0x0005)')
        # ---------------------------------------------------------------------------
        self.feature_0005_index, self.feature_0005, _, _ = DeviceTypeAndNameTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp
# end class BootloaderDeviceTypeAndNameTestCase


class ApplicationDeviceTypeAndNameUsbTestCase(DeviceTypeAndNameTestCaseMixin, DeviceBaseTestCase):
    """
    Validate Device information TestCases in Application mode while the DUT is connected thru USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reload_nvs = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0005 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0005_index, self.feature_0005, _, _ = DeviceTypeAndNameTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp

    @features('Feature0005')
    @features('USB')
    @features('Wireless')
    @level('Business')
    def test_get_full_device_name(self):
        """
        Validate GetDeviceName Business case sequence while the DUT is connected thru USB protocol

        Retrieve the whole device name string
        """
        self.generic_get_full_device_name()

        self.testCaseChecked("FUN_0005_0003")
    # end def test_get_full_device_name
# end class ApplicationDeviceTypeAndNameUsbTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
