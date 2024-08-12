#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.device.connectionscheme.testrunner
    :brief: Device connection scheme tests runner
    :author: Christophe Roquebert
    :date: 2020/03/09
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.connectionscheme.discovery import DiscoveryTestCase
from pytestbox.device.connectionscheme.enumeration import EnumerationTestCase
from pytestbox.device.connectionscheme.pairing import PairingTestCase
from pytestbox.device.connectionscheme.pairing_functionality import PairingFunctionalityTestCase
from pytestbox.device.connectionscheme.pairing_functionality import UnpairingFunctionalityTestCase
from pytestbox.device.connectionscheme.pairing_security import PairingSecurityTestCase
from pytestbox.device.connectionscheme.pairing_robustness import PairingRobustnessTestCase
from pytestbox.device.connectionscheme.connectivity import ConnectivityTestCase
from pytestbox.device.connectionscheme.connectivity_multiplebutton import ConnectivityMultipleButtonTestCase
from pytestbox.device.connectionscheme.safeprepairedreceiver import SafePrePairedRcvrTestCase
from pytestbox.device.connectionscheme.servicechangesupport import ServiceChangeSupportTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConnectionSchemeTestSuite(PyHarnessSuite):
    """
    Device Connection Scheme tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # Device BLE Pro discovery & enumeration features
        self.runTest(result, context, DiscoveryTestCase)
        self.runTest(result, context, EnumerationTestCase)
        # Device BLE Pro pairing feature
        self.runTest(result, context, PairingTestCase)
        self.runTest(result, context, PairingFunctionalityTestCase)
        self.runTest(result, context, UnpairingFunctionalityTestCase)
        self.runTest(result, context, PairingSecurityTestCase)
        self.runTest(result, context, PairingRobustnessTestCase)
        # Device BLE Pro Connection Scheme
        # - Connectivity
        self.runTest(result, context, ConnectivityTestCase)
        self.runTest(result, context, ConnectivityMultipleButtonTestCase)
        # - Safe Pre Paired Receiver
        self.runTest(result, context, SafePrePairedRcvrTestCase)
        # BLE service change support
        self.runTest(result, context, ServiceChangeSupportTestCase)
    # end def runTests

# end class ConnectionSchemeTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
