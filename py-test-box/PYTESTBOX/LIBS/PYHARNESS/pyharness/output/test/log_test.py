#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.logtest

@brief Tests of the LogTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.test.core_test              import TestListenerTestCase
from pyharness.output.logui               import LogTestListener

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LogTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the LogTestListener class
    '''

    @staticmethod
    def isAbstract ():
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
        return LogTestListener
    # end def _getTestListenerClass
# end class LogTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
