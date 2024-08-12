#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.testrunner

@brief  tests testrunner implementation

@author christophe.roquebert

@date   2018/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions                import PyHarnessSuite
from autotests.assertion                 import TestAssertMethods
from autotests.skip                      import SubTestTestCase
from autotests.skip                      import SkippingTestCase
from autotests.skip                      import MySkippedTestCase
from autotests.skip                      import ExpectedFailureTestCase
from autotests.logging                   import LoggingTestCase
from autotests.subsystem.testrunner      import SubsystemTestSuite
from autotests.failure                   import SetUpTearDownTestCase
from autotests.failure                   import FailureTestCase
from autotests.failure                   import ErrorTestCase
from autotests.cleanup                   import AddCleanUpTestCase
from autotests.fixtures                  import FixturesTestCase
from autotests.fixtures                  import FixturesWithStringTestCase
from autotests.newfeatures.testrunner    import NewFeaturesTestRunner
from autotests.newmodules.testrunner     import NewModulesTestRunner

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AutoTestSuite(PyHarnessSuite):
    """
    A test suite that runs the various autotests.
    """

    def canRun(self, unusedresult,                                                                                      #pylint:disable=R0201,W8012
                     context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.canRun
        """
        f = context.getFeatures()
        return f.EXAMPLES.F_Enabled
    # end def canRun

    def runTests(self, result,                                                                                          #pylint:disable=W8012
                       context):
        """
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        """
        # Basic
        self.runTest(result, context, TestAssertMethods)
        self.runTest(result, context, SubTestTestCase)
        self.runTest(result, context, SkippingTestCase)
        self.runTest(result, context, MySkippedTestCase)
        self.runTest(result, context, ExpectedFailureTestCase)
        self.runTest(result, context, SetUpTearDownTestCase)
        self.runTest(result, context, LoggingTestCase)
        self.runTest(result, context, AddCleanUpTestCase)
        self.runTest(result, context, FixturesTestCase)
        self.runTest(result, context, FixturesWithStringTestCase)
        self.runTest(result, context, NewFeaturesTestRunner)
        self.runTest(result, context, NewModulesTestRunner)
        
        # Errors & failures handling
#         self.runTest(result, context, FailureTestCase)   
#         self.runTest(result, context, ErrorTestCase)
        
        # Tests
        self.runTest(result, context, SubsystemTestSuite)
    # end def runTests

# end class AutoTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
