#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.subsystem.test.testrunner

@brief  Tests testrunner implementation

@author christophe Roquebert

@date   2018/02/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions                import PyHarnessSuite
from autotests.subsystem.test.testcases  import TestCasesTestCase

# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class SubsytemTestsTestSuite(PyHarnessSuite):
    '''
    Test runner class for Examples tests
    '''
    def runTests(self, result,
                       context):
        '''
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        '''
        self.runTest(result, context, TestCasesTestCase)
    # end def runTests

# end class SubsytemTestsTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
