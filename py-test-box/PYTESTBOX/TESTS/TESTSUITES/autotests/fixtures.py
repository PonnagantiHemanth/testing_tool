#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package autotests.fixtures

@brief  TFixtures auto tests

@author christophe.roquebert

@date   2018/10/14
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from pyharness.extensions       import PyHarnessCase
from pyharness.fixtures         import fixtures
import inspect
import unittest

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class FixtureConstant():                                                                                # pylint:disable=R0901
    """
    Fixtures constants used in the following tests
    """
    INIT_VALUE              = 1
    # Setup Class fixture parameters
    CLASS_FIXTURE_INCR      = 2
    CLASS_FIXTURE_VALUE     = 3
    # Decorated Class fixture parameters
    CLASS_FIXTURE2_INCR     = 3
    CLASS_FIXTURE2_VALUE    = 6
    # Decorated Test fixture parameters
    METHOD_FIXTURE1_INCR    = 4
    METHOD_FIXTURE1_VALUE   = 10
    METHOD_FIXTURE2_INCR    = 5
    METHOD_FIXTURE2_VALUE   = 15
    # Other decorated Test fixture parameters
    METHOD_FIXTURE3_INCR    = 6
    METHOD_FIXTURE3_VALUE   = 33
# end class FixtureConstant

# --- add a class fixture for all tests
def external_class_fixture(self, value = 0, unused= None, unused_string='empty', 
                                 multiplier=2):
    'class fixture method'
    self.variable += (value * multiplier)
    self.new_class_variable = True
    self.logPoint()
# end def external_class_fixture

class FixturesMixin(PyHarnessCase):                                                                                    # pylint:disable=R0901
    """
    Mixin to share init, setup and logPoint function with both following TestCase class.
    """
    
    def __init__(self, methodName):
        PyHarnessCase.__init__(self, methodName = methodName)
        self.variable = FixtureConstant.INIT_VALUE
        
    def setUp(self):
        'Setup called multiple times, before every test method'
        self.logPoint()
        
        # --- add a class fixture for all tests
        def class_fixture(value = 0, unused= None, unused_string='empty'):
            'class fixture method'
            self.variable += (value)
            self.new_class_variable_in_setup = True
            self.logPoint()
        # end def class_fixture
        self.addFixture(class_fixture, value = FixtureConstant.CLASS_FIXTURE_INCR)
    # end def setUp
    
    def logPoint(self):
        'utility method to trace control flow'
        callingFunction = inspect.stack()[1][3]
        currentTest = self.id().split('.')[-1]
        #print('in %s - %s()' % (currentTest, callingFunction))
        self.logTrace('in %s - %s()' % (currentTest, callingFunction))
        #print('self.variable=%d' % self.variable)
# end FixturesMixin
            
@fixtures(external_class_fixture, unused=True, multiplier=1, value = FixtureConstant.CLASS_FIXTURE2_INCR)
class FixturesTestCase(FixturesMixin):                                                                                    # pylint:disable=R0901
    """
    Fixtures methods can be added from either a decorator 
        @fixtures(...)
    or a setUp method.
        self.addFixture()
    
    Fixtures functions are called just AFTER setUp()
    """
    def test_class_fixture(self):
        '''Test executed after the class fixture method'''
        self.logPoint()
        self.assertEqual(FixtureConstant.CLASS_FIXTURE2_VALUE, self.variable, 
            'Wrong variable value after a class fixture execution')
        self.assertTrue(hasattr(self, 'new_class_variable'), 
            '@fixtures: new attribute not found in test instance')
        self.assertTrue(self.new_class_variable, 
            '@fixtures: variable value not as expected')
        self.assertTrue(hasattr(self, 'new_class_variable_in_setup'), 
            'addFixture: new attribute not found in test instance')
        self.assertTrue(self.new_class_variable_in_setup, 
            'addFixture: variable value not as expected')
    # end def test_class_fixture

    # --- add a fixture method
    def fixture_on_a_test(self, value, unused= None, unused_string='empty', multiplier=1):
        'test specific fixture method'
        self.variable += (value * multiplier)
        self.new_test_variable = True
        self.logPoint()
    # end def fixture_on_a_test

    @fixtures(fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR,
              True, 'test_string', )
    def test_method_fixture_with_string(self):
        'Test executed after the method fixture method'
        self.logPoint()
        expected = FixtureConstant.METHOD_FIXTURE1_VALUE
        self.assertEqual(expected, self.variable, 
            'Wrong variable value after a method fixture execution')
    # end def test_method_fixture_with_string
        
    @unittest.skip("force skipping")
    @fixtures(fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR, )
    def test_fixture_and_skipping(self):
        """ Skipping a test is simply a matter of using 
            the skip() decorator """
        self.fail("shouldn't happen")
    # end def test_skipping

    @fixtures(fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR, )
    def test_method_fixture(self):
        'Test executed after the method fixture method'
        self.logPoint()
        expected = FixtureConstant.METHOD_FIXTURE1_VALUE
        self.assertEqual(expected, self.variable, 
            'Wrong variable value after a method fixture execution')
        self.assertTrue(hasattr(self, 'new_test_variable'), 
            '@fixtures: new attribute not found in test instance')
        self.assertTrue(self.new_test_variable, 
            '@fixtures: variable value not as expected')
    # end def test_method_fixture

    @fixtures(fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR, )
    @fixtures(fixture_on_a_test, FixtureConstant.METHOD_FIXTURE2_INCR, )
    def test_2_consecutive_fixtures(self):
        'Test executed after two consecutive fixtures decorators'
        self.logPoint()
        self.assertEqual(FixtureConstant.METHOD_FIXTURE2_VALUE, self.variable, 
            'Wrong variable value after multiple method fixture execution')
    # end def test_2_consecutive_fixtures
        
    @fixtures((fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR, ), 
              (fixture_on_a_test, FixtureConstant.METHOD_FIXTURE2_INCR, ))
    def test_fixture_2_entries(self):
        'Test executed after two method fixtures included in the same decorator '
        self.logPoint()
        self.assertEqual(FixtureConstant.METHOD_FIXTURE2_VALUE, self.variable, 
            '''Wrong variable value after the execution of 
               two fixtures included in the same decorator''')
    # end def test_fixture_2_entries

    # --- add an other fixture method
    def other_fixture_on_a_test(self, value, multiplier=2):
        'test specific fixture method'
        self.variable += (value * multiplier)
        self.logPoint()
    # end def other_fixture_on_a_test

    @fixtures(fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR, )
    @fixtures(fixture_on_a_test, value=FixtureConstant.METHOD_FIXTURE2_INCR, )
    @fixtures(other_fixture_on_a_test, value=FixtureConstant.METHOD_FIXTURE3_INCR, multiplier=3, )
    def test_3_consecutive_fixtures(self):
        'Test executed after three consecutive fixtures decorators'
        self.logPoint()
        self.assertEqual(FixtureConstant.METHOD_FIXTURE3_VALUE, self.variable, 
            'Wrong variable value after three fixtures execution')
    # end def test_3_consecutive_fixtures
        
    @fixtures((fixture_on_a_test, FixtureConstant.METHOD_FIXTURE1_INCR, ), 
              (fixture_on_a_test, FixtureConstant.METHOD_FIXTURE2_INCR, ),
              (other_fixture_on_a_test, FixtureConstant.METHOD_FIXTURE3_INCR, 3,))
    def test_fixture_3_entries(self):
        'Test executed after three method fixtures included in the same decorator '
        self.logPoint()
        self.assertEqual(FixtureConstant.METHOD_FIXTURE3_VALUE, self.variable, 
            '''Wrong variable value after the execution of 
               three fixtures included in the same decorator''')
    # end def test_fixture_3_entries
        
# end class FixturesTestCase

@fixtures(external_class_fixture, FixtureConstant.CLASS_FIXTURE2_INCR, True, 
          'unused_string', multiplier=1, )
class FixturesWithStringTestCase(FixturesMixin):                                                                                    # pylint:disable=R0901
    """
    Fixture methods shall support string parameter
    """

    def test_class_fixture_with_string(self):
        '''Test executed after the class fixture method'''
        self.logPoint()
        self.assertEqual(FixtureConstant.CLASS_FIXTURE2_VALUE, self.variable, 
            'Wrong variable value after a class fixture execution')
    # end def test_class_fixture_with_string
# end class FixturesWithStringTestCase
    

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
