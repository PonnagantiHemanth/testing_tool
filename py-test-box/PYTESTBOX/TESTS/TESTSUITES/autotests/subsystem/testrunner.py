#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.subsystem.testrunner

@brief  EXAMPLES subsystem testrunner implementation

@author christophe Roquebert

@date   2018/05/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions                import PyHarnessSuite
from autotests.subsystem.test.testrunner import SubsytemTestsTestSuite

# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class SubsystemTestSuite(PyHarnessSuite):
    '''
    Test runner class for Examples tests
    '''
    def runTests(self, result,
                       context):
        '''
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        '''
        self.runTest(result, context, SubsytemTestsTestSuite)
    # end def runTests

# end class SubsystemTestSuite

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
