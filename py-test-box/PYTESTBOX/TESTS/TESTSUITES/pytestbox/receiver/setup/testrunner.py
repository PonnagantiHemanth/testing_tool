#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.setup.testrunner
    :brief: Receiver setup tests runner
    :author: Christophe Roquebert
    :date: 2021/01/27
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.receiver.setup.setup import SetupTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SetupTestSuite(PyHarnessSuite):
    """
    Receiver Setup tests launcher
    """

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        # CI node setup
        self.runTest(result, context, SetupTestCase)
    # end def runTests

# end class SetupTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
