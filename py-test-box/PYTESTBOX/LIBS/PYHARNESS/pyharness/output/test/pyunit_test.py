#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.pyunittest

@brief Tests of the PyUnitTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.test.core_test              import TestListenerTestCase
from pyharness.output.pyunitui            import PyUnitTestListener

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PyUnitTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the PyUnitTestListener class
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
        return PyUnitTestListener
    # end def _getTestListenerClass
# end class PyUnitTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
