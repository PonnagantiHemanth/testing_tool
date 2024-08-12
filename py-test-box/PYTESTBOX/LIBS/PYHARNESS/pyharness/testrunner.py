#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.testrunner

@brief PyHarness main discovery test runner.

@author christophe.roquebert

@date   2018/11/14
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.extensions                         import DiscoveryTestSuite


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PyHarnessTestRunner(DiscoveryTestSuite):
    '''
    A TestSuite that runs all child tests
    '''
# end class PyHarnessTestRunner

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
