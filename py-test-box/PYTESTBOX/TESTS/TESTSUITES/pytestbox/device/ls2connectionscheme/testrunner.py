#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.device.ls2_connectionscheme.testrunner
    :brief: Device ls2 connection scheme tests runner
    :author: Zane Lu
    :date: 2020/10/28
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.ls2connectionscheme.ble_test_cases import BleTestCases
from pytestbox.device.ls2connectionscheme.protocol_switch import ProtocolSwitchTestCases
from pytestbox.device.ls2connectionscheme.oob_test_cases import OobTestCases
from pytestbox.device.ls2connectionscheme.pairing_test_cases import PairingTestCases
from pytestbox.device.ls2connectionscheme.power_on_test_cases import PowerOnTestCases
from pytestbox.device.ls2connectionscheme.reconnection_test_cases import ReconnectionTestCases
from pytestbox.device.ls2connectionscheme.uhs_oob_test_cases import UhsOobTestCases
from pytestbox.device.ls2connectionscheme.uhs_power_on_test_cases import UhsPowerOnTestCases
from pytestbox.device.ls2connectionscheme.uhs_reconnection_test_cases import UhsReconnectionTestCases
from pytestbox.device.ls2connectionscheme.uhs_usb_test_cases import UhsUsbTestCases
from pytestbox.device.ls2connectionscheme.usb_test_cases import UsbTestCases
from pytestbox.device.ls2connectionscheme.force_pairing_test_cases import ForcePairingTestCases
from pytestbox.device.ls2connectionscheme.cs_force_pairing_test_cases import CSForcePairingTestCases

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Ls2ConnectionSchemeTestSuite(PyHarnessSuite):
    """
    Device Connection Scheme tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        #
        self.runTest(result, context, OobTestCases)
        self.runTest(result, context, PowerOnTestCases)
        self.runTest(result, context, ReconnectionTestCases)
        self.runTest(result, context, UsbTestCases)
        self.runTest(result, context, PairingTestCases)
        self.runTest(result, context, ForcePairingTestCases)
        self.runTest(result, context, CSForcePairingTestCases)
        self.runTest(result, context, UhsOobTestCases)
        self.runTest(result, context, UhsPowerOnTestCases)
        self.runTest(result, context, UhsReconnectionTestCases)
        self.runTest(result, context, UhsUsbTestCases)
        self.runTest(result, context, BleTestCases)
        self.runTest(result, context, ProtocolSwitchTestCases)
    # end def runTests

# end class Ls2ConnectionSchemeTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
