#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.tde.testrunner
    :brief: Receiver HID++ tests runner
    :author: Martin Cryonnet
    :date: 2020/02/19
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.tde.prepairing_functionality import PrepairingFunctionalityTestCase
from pytestbox.receiver.tde.prepairing_robustness import PrepairingRobustnessTestCase
from pytestbox.receiver.tde.tde_functionality import TDEFunctionalityTestCase
from pytestbox.receiver.tde.tde_robustness import TDERobustnessTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ReceiverTDETestSuite(PyHarnessSuite):
    """
    Receiver TDE tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # TDE sequence tests
        self.runTest(result, context, TDEFunctionalityTestCase)
        self.runTest(result, context, TDERobustnessTestCase)

        # Prepairing tests
        self.runTest(result, context, PrepairingFunctionalityTestCase)
        self.runTest(result, context, PrepairingRobustnessTestCase)
    # end def runTests
# end class ReceiverTDETestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
