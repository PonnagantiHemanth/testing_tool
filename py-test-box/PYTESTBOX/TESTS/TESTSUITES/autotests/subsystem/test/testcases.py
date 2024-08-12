#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.subsystem.test.testcases

@brief  Validates a TestCase

@author christophe Roquebert

@date   2018/05/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import PyHarnessCase
from pytestbox.base.emulatorsmanager import EmulatorsManager

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

# These constants should be generated automatically in a separate .py file
TESTCASE_SUBSYSTEM_EXAMPLE_1 = "TESTCASE_SUBSYSTEM_EXAMPLE_1"
TESTCASE_SUBSYSTEM_EXAMPLE_2 = "TESTCASE_SUBSYSTEM_EXAMPLE_2"

class TestCasesTestCase(PyHarnessCase):
    '''
    Validates TestCases
    '''

    def testCase1(self):
        '''
        Validates TestCase 1
        '''
        emulators_manager = EmulatorsManager.get_instance(self.getFeatures())
        emulators_manager.init_kosmos()

        self.testCaseChecked(TESTCASE_SUBSYSTEM_EXAMPLE_1, 'roquebert', 'comment')
    # end def testCase1

    def testCase2(self):
        '''
        DOES NOT Validate TestCase 2, though it is referenced
        '''
        if (False):
            self.testCaseChecked(TESTCASE_SUBSYSTEM_EXAMPLE_2)
        # end if
    # end def testCase2
# end class TestCasesTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
