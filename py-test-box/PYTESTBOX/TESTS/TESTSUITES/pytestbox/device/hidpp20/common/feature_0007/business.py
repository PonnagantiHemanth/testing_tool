#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0007.business
:brief: HID++ 2.0 DeviceFriendlyName business test suite
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
class DeviceFriendlyNameBusinessTestCase(DeviceFriendlyNameTestCase):
    """
    Validates DeviceFriendlyName business test cases
    """
    @features('Feature0007')
    @level('Business')
    def test_get_friendly_name_chunk_by_chunk(self):
        """
        Validate GetFriendlyName business case sequence
        """
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)
        self.testCaseChecked("BUS_0007_0001", _AUTHOR)
    # end def test_get_friendly_name_chunk_by_chunk

    @features('Feature0007')
    @level('Business')
    def test_get_default_friendly_name_chunk_by_chunk(self):
        """
        Validate GetDefaultFriendlyName business case sequence
        """
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        Utils.GetDefaultFriendlyNameHelper.HIDppHelper.get_full_name(self, response.default_name_len)
        self.testCaseChecked("BUS_0007_0002", _AUTHOR)
    # end def test_get_default_friendly_name_chunk_by_chunk

    @features('Feature0007')
    @level('Business', 'SmokeTests')
    def test_set_friendly_name(self):
        """
        Validate SetFriendlyName business case sequence
        """
        self.post_requisite_reload_nvs = True
        Utils.SetFriendlyNameHelper.HIDppHelper.set_friendly_name(self, byte_index=0, name_chunk=self.test_name_chunk)
        response = Utils.GetFriendlyNameLenHelper.HIDppHelper.get_friendly_name_len(self)
        received_name = Utils.GetFriendlyNameHelper.HIDppHelper.get_full_name(self, response.name_len)
        Utils.GetFriendlyNameHelper.MessageChecker.check_name_match(self, received_name, self.test_name_chunk)
        self.testCaseChecked("BUS_0007_0003", _AUTHOR)
    # end def test_set_friendly_name
# end class DeviceFriendlyNameBusinessTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
