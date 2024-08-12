#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.junittest

@brief Tests of the JUnitTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.test.core_test              import TestListenerTestCase
from pyharness.output.junitui             import JUnitTestListener
from pyharness.output.junitui             import JUnitLogTestListener

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class JUnitTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the JUnitTestListener class
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
        return JUnitTestListener
    # end def _getTestListenerClass

# end class JUnitTestListenerTestCase


class JUnitLogTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the JUnitLogTestListener class
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
        return JUnitLogTestListener
    # end def _getTestListenerClass

# end class JUnitLogTestListenerTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
