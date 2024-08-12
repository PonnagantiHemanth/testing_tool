#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.small_services.testrunner
:brief: Device BLE GATT small services tests runner
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/11/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.ble.gatt.small_services.business import GattSmallServicesApplicationBusinessTestCase
from pytestbox.device.ble.gatt.small_services.business import GattSmallServicesBootloaderBusinessTestCase
from pytestbox.device.ble.gatt.small_services.errorhandling import GattSmallServicesApplicationErrorHandlingTestCase
from pytestbox.device.ble.gatt.small_services.errorhandling import GattSmallServicesBootloaderErrorHandlingTestCase
from pytestbox.device.ble.gatt.small_services.functionality import GattSmallServicesApplicationFunctionalityTestCase
from pytestbox.device.ble.gatt.small_services.functionality import GattSmallServicesAdvertisingFunctionalityTestCase
from pytestbox.device.ble.gatt.small_services.interface import GattSmallServicesBootloaderInterfaceTestCase
from pytestbox.device.ble.gatt.small_services.interface import GattSmallServicesApplicationInterfaceTestCase
from pytestbox.device.ble.gatt.small_services.robustness import GattSmallServicesRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattSmallServicesTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol small services tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, GattSmallServicesApplicationInterfaceTestCase)
        self.runTest(result, context, GattSmallServicesApplicationBusinessTestCase)
        self.runTest(result, context, GattSmallServicesApplicationFunctionalityTestCase)
        self.runTest(result, context, GattSmallServicesAdvertisingFunctionalityTestCase)
        self.runTest(result, context, GattSmallServicesApplicationErrorHandlingTestCase)
        self.runTest(result, context, GattSmallServicesRobustnessTestCase)

        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, GattSmallServicesBootloaderInterfaceTestCase)
            self.runTest(result, context, GattSmallServicesBootloaderBusinessTestCase)
            self.runTest(result, context, GattSmallServicesBootloaderErrorHandlingTestCase)
        # end if
    # end def runTests
# end class GattSmallServicesTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
