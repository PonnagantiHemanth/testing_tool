#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.looptest

@brief Tests of the LoopTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.input.test.providers_test     import TestProviderTestCase
from pyharness.input.loopui             import LoopTestProvider

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class LoopTestProviderTestCase(TestProviderTestCase):
    '''
    Tests of the LoopTestProvider
    '''

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        return LoopTestProvider()
    # end def _getTestProvider
# end class LoopTestProviderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
