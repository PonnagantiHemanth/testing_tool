#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.testcasesui

@brief  Tests of the DynamicTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.output.testcasesui         import DynamicTestListener
from pyharness.test.core_test              import TestListenerTestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DynamicTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the TESTCASES/*.dynamic TestListener class
    '''

    @staticmethod
    def isAbstract():
        '''
        @copydoc pyharness.test.coretest.TestListenerTestCase.isAbstract
        '''
        return False
    # end def isAbstract

    @staticmethod
    def _getTestListenerClass():
        '''
        @copydoc pyharness.test.coretest.TestListenerTestCase._getTestListenerClass
        '''
        return DynamicTestListener
    # end def _getTestListenerClass
# end class DynamicTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
