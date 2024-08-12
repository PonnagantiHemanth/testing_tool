#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.gatt.device_information
:brief: Device BLE GATT DIS tests runner
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2023/01/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.ble.gatt.device_information.functionality import \
    GattDeviceInformationServiceApplicationFunctionalityTestCase
from pytestbox.device.ble.gatt.device_information.functionality import \
    GattDeviceInformationServiceBootloaderFunctionalityTestCase
from pytestbox.device.ble.gatt.device_information.interface import \
    GattDeviceInformationServiceApplicationInterfaceTestCase
from pytestbox.device.ble.gatt.device_information.interface import \
    GattDeviceInformationServiceBootloaderInterfaceTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class GattDeviceInformationTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol OS detection tests launcher
    """

    def runTests(self, result, context):
        # See ``PyHarnessSuite.runTests``
        self.runTest(result, context, GattDeviceInformationServiceApplicationInterfaceTestCase)
        self.runTest(result, context, GattDeviceInformationServiceApplicationFunctionalityTestCase)
        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, GattDeviceInformationServiceBootloaderInterfaceTestCase)
            self.runTest(result, context, GattDeviceInformationServiceBootloaderFunctionalityTestCase)
        # end if
    # end def runTests
# end class GattDeviceInformationTestSuite
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
