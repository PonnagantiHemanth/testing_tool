#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package autotests.cleanup

@brief  AddCleanup auto tests

@author christophe.roquebert

@date   2018/10/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from pyharness.extensions       import PyHarnessCase
import inspect
import unittest

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AddCleanUpTestCase(PyHarnessCase):                                                                                    # pylint:disable=R0901
    """
    Extra cleanup methods can be added from either a test 
    or a setUp method.
    
    Cleanup functions are called AFTER tearDown()
    """
    def __init__(self, methodName):
        PyHarnessCase.__init__(self, methodName = methodName)
        self.active_test_list = ['test_1', 'test_2', 'test_4', ]
        self.variable = 1
        
    def setUp(self):
        'Setup called multiple times, before every test method'
        self.logPoint()
        
        # --- add a cleanup method fixture for all tests
        def class_cleanup():
            'class cleanUp method'
            self.logPoint()
            test_name = self.id().split('.')[-1]
            self.assertTrue(test_name in self.active_test_list, 
                             'class_cleanup called from the wrong test')
            self.active_test_list.remove(test_name)
        # end def class_cleanup
        self.addCleanup(class_cleanup)
    # end def setUp

    def test_1(self):
        '''Test followed by the test specific cleanUp method 
            then by the class cleanUp method'''
        self.logPoint()
        # --- add a cleanup method fixture for just this test
        def test_cleanup():
            'test specific cleanUp method'
            self.logPoint()
            self.assertEqual('test_1', self.id().split('.')[-1], 
                             'test_cleanup called from the wrong test')
        # end def test_cleanup
        self.addCleanup(test_cleanup)
    # end def test_1

    def test_2(self):
        'Test followed by the class cleanUp method'
        self.logPoint()
    # end def test_2
        
    @unittest.skip("force skipping")
    def test_3(self):
        """ Skipping a test is simply a matter of using 
            the skip() decorator """
        self.fail("shouldn't happen")
    # end def test_3

    def _test_4(self):
        '''Exception in the test specific cleanUp method'''
        self.logPoint()
        # --- add a cleanup method fixture for just this test
        def test_cleanup_with_exception():
            'test specific cleanUp method'
            self.assertEqual(1, 0, "Check error is caught during cleanup")
        # end def test_cleanup_with_exception
        self.addCleanup(test_cleanup_with_exception)
    # end def test_4
 
    def logPoint(self):
        'utility method to trace control flow'
        callingFunction = inspect.stack()[1][3]
        currentTest = self.id().split('.')[-1]
        #print('in %s - %s()' % (currentTest, callingFunction))
        self.logTrace('in %s - %s()' % (currentTest, callingFunction))
        #print('self.variable=%d' % self.variable)
# end class AddCleanUpTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
