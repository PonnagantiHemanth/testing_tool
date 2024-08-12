#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.newmoduls.testrunner

@brief  autotests new modules testrunner implementation

@author christophe Roquebert

@date   2018/05/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions                import PyHarnessSuite
from autotests.newmodules.secrets        import TestSecretsMethods

# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class NewModulesTestRunner(PyHarnessSuite):
    '''
    Test runner class for Python New Modules tests
    '''
    def runTests(self, result,
                       context):
        '''
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        '''
        self.runTest(result, context, TestSecretsMethods)
    # end def runTests

# end class NewModulesTestRunner

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
