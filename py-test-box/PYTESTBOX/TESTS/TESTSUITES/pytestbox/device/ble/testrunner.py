#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.testrunner
:brief: Device BLE Protocol tests runner
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2021/06/23
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ble.advertising.testrunner import BleAdvertisingTestSuite
from pytestbox.device.ble.cccds.testrunner import BleppCccdToggledTestSuite
from pytestbox.device.ble.connection_parameters.testrunner import ConnectionParametersTestSuite
from pytestbox.device.ble.descriptors import DescriptorsTestCases
from pytestbox.device.ble.disconnection import DisconnectionShutdownTestCases
from pytestbox.device.ble.gatt.testrunner import BleGattTestSuite
from pytestbox.device.ble.osdetection.testrunner import BleOsDetectionTestSuite
from pytestbox.device.ble.pairing.testrunner import PairingTestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleProtocolTestSuite(PyHarnessSuite):
    """
    Device BLE Protocol tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, BleAdvertisingTestSuite)
        self.runTest(result, context, BleGattTestSuite)
        self.runTest(result, context, BleppCccdToggledTestSuite)
        self.runTest(result, context, BleOsDetectionTestSuite)
        self.runTest(result, context, ConnectionParametersTestSuite)
        self.runTest(result, context, DescriptorsTestCases)
        self.runTest(result, context, PairingTestSuite)
        self.runTest(result, context, DisconnectionShutdownTestCases)
    # end def runTests
# end class BleProtocolTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
