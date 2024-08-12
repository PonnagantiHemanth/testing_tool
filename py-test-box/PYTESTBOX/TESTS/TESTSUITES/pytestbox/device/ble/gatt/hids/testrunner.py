#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.hids.testrunner
:brief: Device BLE GATT HIDS tests runner
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/03/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.ble.gatt.hids.errorhandling import GattHIDSApplicationErrorHandlingTestCase
from pytestbox.device.ble.gatt.hids.errorhandling import GattHIDSBootloaderErrorHandlingTestCase
from pytestbox.device.ble.gatt.hids.functionality import GattHIDSApplicationFunctionalityTestCase
from pytestbox.device.ble.gatt.hids.functionality import GattHIDSBootloaderFunctionalityTestCase
from pytestbox.device.ble.gatt.hids.interface import GattHIDSApplicationInterfaceTestCase
from pytestbox.device.ble.gatt.hids.interface import GattHIDSBootloaderInterfaceTestCase
# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class GattHIDSTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol OS detection tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, GattHIDSApplicationInterfaceTestCase)
        self.runTest(result, context, GattHIDSApplicationFunctionalityTestCase)
        self.runTest(result, context, GattHIDSApplicationErrorHandlingTestCase)

        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, GattHIDSBootloaderInterfaceTestCase)
            self.runTest(result, context, GattHIDSBootloaderFunctionalityTestCase)
            self.runTest(result, context, GattHIDSBootloaderErrorHandlingTestCase)
        # end if
    # end def runTests
# end class GattHIDSTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
