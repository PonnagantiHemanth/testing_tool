#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
''' @package testrunner

@brief The root test runner.

@author christophe Roquebert

@date   2018/09/13
'''
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions            import PyHarnessSuite
   
# --- test harness auto test ---
from autotests.testrunner            import AutoTestSuite
# --- test harness demo test ---
from pytestbox.testrunner            import DemoTestSuite

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class RootTestRunner(PyHarnessSuite):
    """
    Main suite

    If you want to explicitly call a child test suite or test, you
    need to override the runTests method, and inherit from PyHarnessSuite.

    Tests distributions Vs Config.
    """
    
    def runTests(self, result, context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        # --- test harness demo test --- 
        self.runTest(result, context, DemoTestSuite)

        # --- test harness auto test ---
        self.runTest(result, context, AutoTestSuite)
    # end def runTests

# end class RootTestRunner

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
