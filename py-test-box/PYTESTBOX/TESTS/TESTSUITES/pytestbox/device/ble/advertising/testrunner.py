#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.advertising.testrunner
:brief: Device BLE Protocol advertising tests runner
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2022/05/03
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.ble.advertising.business import AdvertisingApplicationReconnectionBusinessTestCases
from pytestbox.device.ble.advertising.business import AdvertisingBootloaderReconnectionBusinessTestCases
from pytestbox.device.ble.advertising.business import AdvertisingPairingModeNoPrepairingDataBusinessTestCase
from pytestbox.device.ble.advertising.business import AdvertisingPairingModeUnusedPrepairingDataBusinessTestCase
from pytestbox.device.ble.advertising.business import AdvertisingPairingModeUsedPrepairingDataBusinessTestCase
from pytestbox.device.ble.advertising.functionality import AdvertisingApplicationReconnectionFunctionalityTestCases
from pytestbox.device.ble.advertising.functionality import AdvertisingBootloaderReconnectionFunctionalityTestCases
from pytestbox.device.ble.advertising.functionality import AdvertisingPairingModeNoPrepairingDataFunctionalityTestCases
from pytestbox.device.ble.advertising.interface import AdvertisingApplicationReconnectionInterfaceTestCase
from pytestbox.device.ble.advertising.interface import AdvertisingBootloaderReconnectionInterfaceTestCase
from pytestbox.device.ble.advertising.interface import AdvertisingPairingModeNoPrepairingDataInterfaceTestCase
from pytestbox.device.ble.advertising.interface import AdvertisingPairingModeUnusedPrepairingDataInterfaceTestCase
from pytestbox.device.ble.advertising.interface import AdvertisingPairingModeUsedPrepairingDataInterfaceTestCase
from pytestbox.device.ble.advertising.robustness import AdvertisingApplicationReconnectionModeRobustnessTestCase
from pytestbox.device.ble.advertising.robustness import AdvertisingBootloaderReconnectionModeRobustnessTestCase
from pytestbox.device.ble.advertising.robustness import AdvertisingPairingModeNoPrepairingDataRobustnessTestCases
from pytestbox.device.ble.advertising.robustness import AdvertisingPairingModeUnusedPrepairingDataRobustnessTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleAdvertisingTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol advertising tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # Advertising pairing mode with no prepairing data
        self.runTest(result, context, AdvertisingPairingModeNoPrepairingDataInterfaceTestCase)
        self.runTest(result, context, AdvertisingPairingModeNoPrepairingDataBusinessTestCase)
        self.runTest(result, context, AdvertisingPairingModeNoPrepairingDataFunctionalityTestCases)
        self.runTest(result, context, AdvertisingPairingModeNoPrepairingDataRobustnessTestCases)

        if context.getFeatures().PRODUCT.PROTOCOLS.BLE_PRO.F_Enabled:
            # Advertising pairing mode with unused prepairing data
            self.runTest(result, context, AdvertisingPairingModeUnusedPrepairingDataInterfaceTestCase)
            self.runTest(result, context, AdvertisingPairingModeUnusedPrepairingDataBusinessTestCase)
            self.runTest(result, context, AdvertisingPairingModeUnusedPrepairingDataRobustnessTestCase)

            # Advertising pairing mode with used prepairing data
            self.runTest(result, context, AdvertisingPairingModeUsedPrepairingDataInterfaceTestCase)
            self.runTest(result, context, AdvertisingPairingModeUsedPrepairingDataBusinessTestCase)
        # end if

        # Advertising application reconnection mode (no RPA)
        self.runTest(result, context, AdvertisingApplicationReconnectionInterfaceTestCase)
        self.runTest(result, context, AdvertisingApplicationReconnectionBusinessTestCases)
        self.runTest(result, context, AdvertisingApplicationReconnectionFunctionalityTestCases)
        self.runTest(result, context, AdvertisingApplicationReconnectionModeRobustnessTestCase)

        # Advertising bootloader reconnection mode (no RPA)
        config_manager = ConfigurationManager(context.getFeatures())
        if config_manager.feature_value_map[config_manager.ID.TRANSPORT_BTLE][config_manager.MODE.BOOTLOADER]:
            self.runTest(result, context, AdvertisingBootloaderReconnectionInterfaceTestCase)
            self.runTest(result, context, AdvertisingBootloaderReconnectionBusinessTestCases)
            self.runTest(result, context, AdvertisingBootloaderReconnectionFunctionalityTestCases)
            self.runTest(result, context, AdvertisingBootloaderReconnectionModeRobustnessTestCase)
        # end if
    # end def runTests
# end class BleAdvertisingTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
