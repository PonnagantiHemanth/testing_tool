#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.interface
:brief: HID++ 2.0  Device Secure DFU control interface test suite
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
class DeviceSecureDfuControlInterfaceTestCase(DeviceSecureDfuControlTestCase):
    """
    Validate Secure DFU Control interface testcases for the device (feature 0x00C3).
    """

    @features('SecureDfuControlAllActionTypes')
    @level('Interface')
    @services('Debugger')
    def test_get_dfu_control_no_dfu_chunk_api(self):
        """
        getDfuControl API validation when no DFU chunk in NVS

        [0] getDfuControl() -> enableDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
        """
        self.generic_get_dfu_control_no_dfu_chunk_api()

        self.testCaseChecked("INT_00C3_0001")
    # end def test_get_dfu_control_no_dfu_chunk_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_get_dfu_control_dfu_enabled_in_nvs_api(self):
        """
        getDfuControl API validation when DFU enabled in NVS

        [0] getDfuControl() -> enableDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
        """
        self.generic_get_dfu_control_dfu_enabled_in_nvs_api()

        self.testCaseChecked("INT_00C3_0002")
    # end def test_get_dfu_control_dfu_enabled_in_nvs_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_get_dfu_control_dfu_disabled_in_nvs_api(self):
        """
        getDfuControl API validation when DFU disabled in NVS

        [0] getDfuControl() -> enableDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
        """
        self.generic_get_dfu_control_dfu_disabled_in_nvs_api()

        self.testCaseChecked("INT_00C3_0003")
    # end def test_get_dfu_control_dfu_disabled_in_nvs_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_set_dfu_control_enable_dfu_api(self):
        """
        setDfuControl API validation with DFU enable when no DFU chunk in NVS

        [1] setDfuControl(enableDfu, dfuControlParam, dfuMagicKey)
        """
        self.generic_set_dfu_control_enable_dfu_api()

        self.testCaseChecked("INT_00C3_0004")
    # end def test_set_dfu_control_enable_dfu_api

    @features('SecureDfuControlUseNVS')
    @level('Interface')
    @services('Debugger')
    def test_set_dfu_control_disable_dfu_api(self):
        """
        setDfuControl API validation with DFU disable when no DFU chunk in NVS

        [1] setDfuControl(enableDfu, dfuControlParam, dfuMagicKey)
        """
        self.generic_set_dfu_control_disable_dfu_api()

        self.testCaseChecked("INT_00C3_0005")
    # end def test_set_dfu_control_disable_dfu_api
# end class DeviceSecureDfuControlInterfaceTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
