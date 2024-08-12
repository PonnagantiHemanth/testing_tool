#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.testrunner
:brief: Device BLE Protocol GATT tests runner
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/07/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ble.gatt.ble_pro.testrunner import GattBleProTestSuite
from pytestbox.device.ble.gatt.device_information.testrunner import GattDeviceInformationTestSuite
from pytestbox.device.ble.gatt.hids.testrunner import GattHIDSTestSuite
from pytestbox.device.ble.gatt.small_services.testrunner import GattSmallServicesTestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleGattTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol GATT tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, GattSmallServicesTestSuite)
        self.runTest(result, context, GattDeviceInformationTestSuite)
        self.runTest(result, context, GattHIDSTestSuite)
        self.runTest(result, context, GattBleProTestSuite)
    # end def runTests
# end class BleGattTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
