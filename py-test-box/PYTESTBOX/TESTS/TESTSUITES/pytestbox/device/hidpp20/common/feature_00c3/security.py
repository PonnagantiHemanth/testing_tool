#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.security
:brief: HID++ 2.0  Device Secure DFU control security test suite
:author: Stanislas Cottard <scottard@logitech.com>, Kevin Dayet <kdayet@logitech.com>
:date: 2020/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pytestbox.device.hidpp20.common.feature_00c3.securedfucontrol import DeviceSecureDfuControlTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceSecureDfuControlSecurityTestCase(DeviceSecureDfuControlTestCase):
    """
    Validate Secure DFU Control security testcases for the device (feature 0x00C3).
    """

    @features('SecureDfuControlUseNVS')
    @level('Security')
    @services('Debugger')
    def test_get_dfu_control_enable_in_nvs_superior_to_1(self):
        """
        getDfuControl when enable byte value greater than 1 in NVS but with enable bit to 1 should return enable = 1
        and all reserved bit to 0
        """
        self.generic_get_dfu_control_enable_in_nvs_superior_to_1()

        self.testCaseChecked("SEC_00C3_0001")
    # end def test_get_dfu_control_enable_in_nvs_superior_to_1

    @features('SecureDfuControlUseNVS')
    @level('Security')
    @services('Debugger')
    def test_entering_dfu_enable_in_nvs_superior_to_1(self):
        """
        getDfuControl when enable byte value greater than 1 in NVS but with enable bit to 1. Check device is in
        bootloader mode after the reset performed with the requested user actions
        """
        self.generic_entering_dfu_enable_in_nvs_superior_to_1()

        self.testCaseChecked("SEC_00C3_0002")
    # end def test_entering_dfu_enable_in_nvs_superior_to_1
# end class DeviceSecureDfuControlSecurityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
