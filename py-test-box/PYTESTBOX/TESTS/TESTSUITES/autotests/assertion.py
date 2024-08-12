#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.assertion

@brief Auto Test of assertion calls

@author christophe.roquebert

@date   2018/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.core  import TestCase
from pyharness.core  import TestException
from pyharness.core  import TYPE_FAILURE
from random         import randint

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class TestAssertMethods(TestCase):
    """ The TestCase class provides several assert methods 
        to check for and report failures. The following tests 
        lists the most commonly used methods. 
            Method                   Checks that          New in
            assertEqual(a, b)        a == b     
            assertNotEqual(a, b)     a != b     
            assertTrue(x)            bool(x) is True     
            assertFalse(x)           bool(x) is False     
            assertIs(a, b)           a is b                3.1
            assertIsNot(a, b)        a is not b            3.1
            assertIsNone(x)          x is None             3.1
            assertIsNotNone(x)       x is not None         3.1
            assertIn(a, b)           a in b                3.1
            assertNotIn(a, b)        a not in b            3.1
            assertIsInstance(a, b)   isinstance(a, b)      3.2
            assertNotIsInstance(a, b) not isinstance(a, b) 3.2"""

    def test_assertEqual(self):
        """ test assertEqual() assert methods """
        a = randint(0, 0xFF)
        b = a
        self.assertEqual(a, b)
    # end def test_assertEqual

    def test_assertNotEqual(self):
        """ test assertNotEqual() assert methods """
        a = randint(0, 0xFF)
        b = -1
        self.assertNotEqual(a, b)
    # end def test_assertNotEqual
    
    def test_assertTrue(self):
        """ test assertTrue() assert methods """
        a = True
        self.assertTrue(a)
    # end def test_assertEqual
    
    def test_assertFalse(self):
        """ test assertFalse() assert methods """
        a = False
        self.assertFalse(a)
    # end def test_assertFalse
    
    def test_assertIs(self):
        """ test assertIs() assert methods """
        a = True
        self.assertIs(a, True)
    # end def test_assertIs
    
    def assertIsNonetest_assertIsNot(self):
        """ test assertIsNot() assert methods """
        a = True
        self.assertIsNot(a, False)
    # end def test_assertIsNot
    
    def test_assertIsNone(self):
        """ test assertIsNone() assert methods """
        a = None
        self.assertIsNone(a)
    # end def test_assertIsNot
    
    def test_assertIsNotNone(self):
        """ test assertIsNotNone() assert methods """
        a = 0
        self.assertIsNotNone(a)
    # end def test_assertIsNotNone
    
    def test_assertIn(self):
        """ test assertIn() assert methods """
        a = 8
        self.assertIn(a, range(0, 10, 2))
    # end def test_assertIn
    
    def test_assertNotIn(self):
        """ test assertNotIn() assert methods """
        a = 1
        self.assertNotIn(a, range(0, 10, 2))
    # end def test_assertNotIn
    
    def test_assertIsInstance(self):
        """ test assertIsInstance() assert methods """
        self.assertIsInstance(self, TestCase)
    # end def test_assertIsInstance
    
    def test_assertNotIsInstance(self):
        """ test assertNotIsInstance() assert methods """
        self.assertNotIsInstance(self, int)
    # end def test_assertNotIsInstance
    
    def test_assertRaises(self):
        """ test assertRaises() assert methods """
        s = 'hello world'
        self.assertRaises(TypeError, s.split, 2)
    # end def test_assertRaises
    
# end class TestAssertMethods  
         
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
