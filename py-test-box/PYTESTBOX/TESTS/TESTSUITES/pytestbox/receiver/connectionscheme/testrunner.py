#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.connectionscheme.testrunner
    :brief: Receiver connection scheme tests runner
    :author: Christophe Roquebert
    :date: 2020/02/19
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.connectionscheme.enumeration import EnumerationTestCase
from pytestbox.receiver.connectionscheme.discovery import DiscoveryTestCase
from pytestbox.receiver.connectionscheme.pairing import PairingTestCase
from pytestbox.receiver.connectionscheme.pairing_functionality import PairingFunctionalityTestCase
from pytestbox.receiver.connectionscheme.pairing_functionality import UnpairingFunctionalityTestCase
from pytestbox.receiver.connectionscheme.pairing_security import PairingSecurityTestCase
from pytestbox.receiver.connectionscheme.pairing_robustness import PairingRobustnessTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConnectionSchemeTestSuite(PyHarnessSuite):
    """
    Receiver Connection Scheme tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # Paired device enumeration feature
        self.runTest(result, context, EnumerationTestCase)

        # Device discovery feature
        self.runTest(result, context, DiscoveryTestCase)

        # Device pairing feature
        self.runTest(result, context, PairingTestCase)
        self.runTest(result, context, PairingFunctionalityTestCase)
        self.runTest(result, context, UnpairingFunctionalityTestCase)
        self.runTest(result, context, PairingSecurityTestCase)
        self.runTest(result, context, PairingRobustnessTestCase)
    # end def runTests

# end class ConnectionSchemeTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
