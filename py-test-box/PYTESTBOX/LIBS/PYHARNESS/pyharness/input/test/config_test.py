#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.configtest

@brief Tests of the ConfigTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.input.test.providers_test     import TestProviderTestCase
from pyharness.input.configui           import ConfigTestProvider

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class ConfigTestProviderTestCase(TestProviderTestCase):
    '''
    Tests of the ConfigTestProvider
    '''

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        return ConfigTestProvider()
    # end def _getTestProvider
# end class ConfigTestProviderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
