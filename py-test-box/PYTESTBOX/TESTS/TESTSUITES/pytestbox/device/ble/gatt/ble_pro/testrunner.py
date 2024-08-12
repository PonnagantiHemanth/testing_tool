#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.ble_pro.testrunner
:brief: Device BLE GATT BLE Pro tests runner
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/06/29
"""


# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.ble.gatt.ble_pro.errorhandling import GattBleProApplicationErrorHandlingTestCase
from pytestbox.device.ble.gatt.ble_pro.errorhandling import GattBleProBootloaderErrorHandlingTestCase
from pytestbox.device.ble.gatt.ble_pro.functionality import GattBleProApplicationFunctionalityPairingTestCase
from pytestbox.device.ble.gatt.ble_pro.functionality import GattBleProApplicationFunctionalityTestCase
from pytestbox.device.ble.gatt.ble_pro.interface import GattBleProInterfaceApplicationTestCase
from pytestbox.device.ble.gatt.ble_pro.interface import GattBleProInterfaceBootloaderTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattBleProTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol small services tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, GattBleProInterfaceApplicationTestCase)
        self.runTest(result, context, GattBleProApplicationFunctionalityTestCase)
        self.runTest(result, context, GattBleProApplicationFunctionalityPairingTestCase)
        self.runTest(result, context, GattBleProApplicationErrorHandlingTestCase)

        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, GattBleProBootloaderErrorHandlingTestCase)
            self.runTest(result, context, GattBleProInterfaceBootloaderTestCase)
        # end if
    # end def runTests
# end class GattSmallServicesTestSuite
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
