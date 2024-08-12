#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.tools.testrunner
:brief: Tools tests runner
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2023/07/20
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.tools.kosmos.testrunner import KosmosTestSuite
from pytestbox.tools.nrfblelib import NrfBleLibTestCase
from pytestbox.tools.rgbconfiguration.testrunner import RgbConfigurationTools


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ToolsTestSuite(PyHarnessSuite):
    """
    Test runner class for Tools tests
    """
    def canRun(self, unusedresult, context):
        """
        Tests whether the test is allowed to run.
        """
        f = context.getFeatures()
        return f.PRODUCT.F_Enabled
    # end def canRun

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.
        """
        self.runTest(result, context, KosmosTestSuite)
        self.runTest(result, context, RgbConfigurationTools)
        self.runTest(result, context, NrfBleLibTestCase)
    # end def runTests
# end class ToolsTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
