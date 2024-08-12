#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.xmltest

@brief Tests of the XmlTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.test.core_test              import TestListenerTestCase
from pyharness.output.xmlui               import XmlTestListener

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class XmlTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the XmlTestListener class
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
        return XmlTestListener
    # end def _getTestListenerClass
# end class XmlTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
