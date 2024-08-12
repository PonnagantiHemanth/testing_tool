#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.stdouttest

@brief Tests of the StdoutTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.test.core_test              import TestListenerTestCase
from pyharness.output.stdoutui            import StdoutTestListener
from io import StringIO

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class StdoutTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the StdoutTestListener class
    '''

    class TestStdoutTestListener(StdoutTestListener):
        '''
        Class overriding stdout for the tests
        '''
        _stdout = StringIO()
    # end class TestStdoutTestListener

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
        return StdoutTestListenerTestCase.TestStdoutTestListener
    # end def _getTestListenerClass
# end class StdoutTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
