#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.newfeatures.testrunner

@brief  autotests newfeatures testrunner implementation

@author christophe Roquebert

@date   2018/05/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions                import PyHarnessSuite
from autotests.newfeatures.strings       import TestStringMethods
from autotests.newfeatures.literals      import TestLiteralsMethods
from autotests.newfeatures.generator     import TestGeneratorsMethods

# ----------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------
class NewFeaturesTestRunner(PyHarnessSuite):
    '''
    Test runner class for Python New Features tests
    '''
    def runTests(self, result,
                       context):
        '''
        @copydoc pyharness.extensions.PyHarnessSuite.runTests
        '''
        self.runTest(result, context, TestStringMethods)
        self.runTest(result, context, TestLiteralsMethods)
        self.runTest(result, context, TestGeneratorsMethods)
    # end def runTests

# end class NewFeaturesTestRunner

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
