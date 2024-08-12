#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.business
:brief: HID++ 2.0  Device Secure DFU control business test suite
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
class DeviceSecureDfuControlBusinessTestCase(DeviceSecureDfuControlTestCase):
    """
    Validates Secure DFU Control  business testcases for the device (feature 0x00C3).
    """
    @features('SecureDfuControlAllActionTypes')
    @level('Business', 'SmokeTests')
    @services('Debugger')
    def test_dfu_control_business(self):
        """
        DFU Control business case when enable DFU mode is requested. Check device is in bootloader mode after a reset
        is performed with the requested user actions. Check 0xD0 feature is advertised in bootloader mode. Check DFU
        status LED starts blinking when entering bootloader mode and stops immediately when it leaves this mode.
        """
        self.generic_dfu_control_business()

        self.testCaseChecked("BUS_00C3_0001")
    # end def test_dfu_control_business
# end class DeviceSecureDfuControlBusinessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
