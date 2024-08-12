#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.discovery.discovery

@brief Tests of the DiscoveryTestSuite class

@author christophe.roquebert

@date   2018/01/17
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions import DiscoveryTestSuite as DTS
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DiscoveryTestSuite(DTS):
    '''
    A class that auto-discovers the tests in the current directory.
    '''
    pass
# end class DiscoveryTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
