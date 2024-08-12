#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.discovery.test2

@brief First test of the discovery suite

@author christophe.roquebert

@date   2018/01/17
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest import TestCase
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class Test2(TestCase):
    '''
    A dummy test
    '''

    def test_discovery(self):
        '''
        Should be called by the discovery runner
        '''
        pass
    # end def test_discovery
# end class Test2

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
