#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.texttest

@brief Tests of the TextTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.input.test.providers_test     import TestProviderTestCase
from pyharness.input.textui             import TextTestProvider

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class TextTestProviderTestCase(TestProviderTestCase):
    '''
    Tests of the TextTestProvider
    '''

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        return TextTestProvider()
    # end def _getTestProvider

# end class TextTestProviderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
