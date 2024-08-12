#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.systemstest

@brief  Systems and modules test implementation

This module tests the SubSystem class, that handles the features.

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.systems                  import AbstractSubSystem
from unittest                           import TestCase
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class SubSystemTestCase( TestCase ):
    '''
    Test the SubSystem class
    '''

    def test_CreationWithName(self):
        '''
        SubSystem creation, with assigned name
        '''

        subSystem = AbstractSubSystem("TEST_SUBSYSTEM")
        self.assertEqual("TEST_SUBSYSTEM", subSystem.getName(), "Invalid name")
    # end def test_CreationWithName

    def test_Clone(self):
        '''
        SubSystem cloning
        '''

        subSystem = AbstractSubSystem("TEST_SUBSYSTEM")
        subSystem.testValue = "13456"                                                                                   # pylint:disable=W0201

        def testFunction(unused):
            '''
            Dummy function.

            @param unused [in] (object) Unused parameter
            '''
            pass
        # end def testFunction
        subSystem.testFunction = testFunction                                                                           # pylint:disable=W0201
        subSystem.testMethod = self.test_Clone                                                                          # pylint:disable=W0201

        copy = subSystem.clone()
        self.assertEqual(False,
                         hasattr(copy, "testFunction"),
                         "Function member has been cloned")

        self.assertEqual(False,
                         hasattr(copy, "testMethod"),
                         "Method member has been cloned")

        self.assertEqual(True,
                         hasattr(copy, "testValue"),
                         "Variable member has not been cloned")
    # end def test_Clone
# end class SubSystemTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
