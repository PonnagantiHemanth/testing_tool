#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.test.configtest

@brief Tests of the ConfigTestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.test.core_test              import TestListenerTestCase
from pyharness.output.configui            import ConfigTestListener

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConfigTestListenerTestCase(TestListenerTestCase):
    '''
    Tests of the Settings.ini TestListener class
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
        return ConfigTestListener
    # end def _getTestListenerClass
# end class ConfigTestListenerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
