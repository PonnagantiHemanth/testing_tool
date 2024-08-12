#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.interface
:brief: HID++ 2.0 DeviceFriendlyName interface test suite
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/10/13
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pytestbox.device.base.devicefriendlynameutils import DeviceFriendlyNameTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_0007.devicefriendlyname import DeviceFriendlyNameTestCase

# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Suresh Thiyagarajan"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceFriendlyNameInterfaceTestCase(DeviceFriendlyNameTestCase):
    """
    Validates DeviceFriendlyName interface test cases
    """
    @features('Feature0007')
    @level('Interface')
    def test_get_friendly_name_len(self):
        """
        Validates GetFriendlyNameLen interface
        """
        Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        self.testCaseChecked("INT_0007_0001", _AUTHOR)
    # end def test_get_friendly_name_len

    @features('Feature0007')
    @level('Interface')
    def test_get_friendly_name(self):
        """
        Validates GetFriendlyName interface
        """
        Utils.GetFriendlyNameHelper.HIDppHelper.get_friendly_name(self, byte_index=0)
        self.testCaseChecked("INT_0007_0002", _AUTHOR)
    # end def test_get_friendly_name

    @features('Feature0007')
    @level('Interface')
    def test_get_default_friendly_name(self):
        """
        Validates GetDefaultFriendlyName interface
        """
        Utils.GetDefaultFriendlyNameHelper.HIDppHelper.get_default_friendly_name(self, byte_index=0)
        self.testCaseChecked("INT_0007_0003", _AUTHOR)
    # end def test_get_default_friendly_name

    @features('Feature0007')
    @level('Interface')
    def test_set_friendly_name(self):
        """
        Validates SetFriendlyName interface
        """
        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        self.testCaseChecked("INT_0007_0004", _AUTHOR)
    # end def test_set_friendly_name

    @features('Feature0007')
    @level('Interface')
    def test_reset_friendly_name(self):
        """
        Validates ResetFriendlyName interface
        """
        self.post_requisite_reload_nvs = False
        Utils.ResetFriendlyNameHelper.HIDppHelper.reset_friendly_name(self)
        self.testCaseChecked("INT_0007_0005", _AUTHOR)
    # end def test_set_friendly_name
# end class DeviceFriendlyNameInterfaceTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
