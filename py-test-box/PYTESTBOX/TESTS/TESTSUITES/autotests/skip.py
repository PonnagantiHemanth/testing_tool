#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.skip

@brief Auto Test targeting Skipping and expected failures handling

@author christophe.roquebert

@date   2018/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyharness.core  import TestCase
import unittest
#import pyhid
import sys
# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
    
def skipIfHasattr(obj, attr):
    """ It's easy to roll your own skipping decorators by 
        making a decorator that calls skip() on the test """
    if hasattr(obj, attr):
        return unittest.skip("{!r} does have a {!r} attribute".format(obj, attr))
    return lambda func: func
# end def skipIfHasattr


class SkippingTestCase(TestCase):
    """ Unittest supports skipping individual test methods 
        and even whole classes of autotests."""
        
    def setUp(self):
        """ TestCase.setUp() can also skip the test. 
            This is useful when a resource that needs to be set up 
            is not available. """
        if self._testMethodName == 'test_skip_in_setUp':
            # Usually you can use TestCase.skipTest() or one 
            # of the skipping decorators instead of raising this directly.
            TestCase.skipTest(self, "setUp calls TestCase.skipTest()")
            #raise SkipTest
        # end if
    # end def setUp
    
    @unittest.skip("demonstrating skipping")
    def test_skip_decoractor(self):
        """ Skipping a test is simply a matter of using 
            the skip() decorator """
        self.fail("shouldn't happen")
    # end def test_skip_decoractor
        
    @unittest.skipIf(True, #pyhid.__version__ < (0, 5, 2),
                     "not supported in this library version")
    def test_skipIf_variant(self):
        """ Skipping a test is simply a matter of using 
            a conditional variants of the skip() decorator """
        # Tests that work for only a certain version of the library.
        # Force a fail to check following is never executed
        self.fail("shouldn't happen")
    # end def test_skipIf_variant
    
    @unittest.skipUnless(not sys.platform.startswith("win") and 
                         not sys.platform.startswith("linux") and
                         not sys.platform.startswith("darwin"),
                         "not supported on Windows, Linux and Darwin")
    def test_skipUnless_variant(self):
        """ Skipping a test is simply a matter of using 
            a conditional variants of the skip() decorator """
        # windows excluded testing code
        # Force a fail to check following is never executed
        self.fail("shouldn't happen")
    # end def test_skipUnless_variant
    
    @skipIfHasattr(TestCase, 'failureException')
    def test_skipIfHasattr_variant(self):
        """ Skipping a test is simply a matter of using 
            a customized skip decorator """
        # windows excluded testing code
        # Force a fail to check following is never executed
        self.fail("shouldn't happen")
    # end def test_skipIfHasattr_variant
    
    def test_skip_in_setUp(self):
        """ TestCase.setUp() can also skip the test. 
            This is useful when a resource that needs to be set up 
            is not available. """
        # Force a fail to check following is never executed
        self.fail("shouldn't happen")
    # end def test_skip_in_setUp
    
    def test_skipTest(self):
        """ Usually you can use TestCase.skipTest() or one 
        # of the skipping decorators instead of raising this directly. """
        # call skipTest Exception.
        TestCase.skipTest(self, "def test calls TestCase.skipTest()")
        # Force a fail to check following is never executed
        self.fail("shouldn't happen")
    # end def test_skip_in_setUp
    
# end class SkippingTestCase


@unittest.skip("showing class skipping")
class MySkippedTestCase(unittest.TestCase):
    """  Classes can be skipped just like methods """
    def test_not_run_due_to_skipped_class(self):
        # Force a fail to check following is never executed
        self.fail("shouldn't happen")
    # end def test_not_run_due_to_skipped_class
# end class MySkippedTestCase


class SubTestTestCase(TestCase):
    """ Distinguishing test iterations using subtests """
    
    def test_subTest(self):
        """
        Test that numbers between 0 and 5 are all even.
        """
        for i in range(0, 6, 2):
            with self.subTest(i=i):
                self.assertEqual(i % 2, 0, "Wrong assertion with i=%d" % i)
            # end with
        # end for
    # end def test_even
# end class SubTestTestCase


class ExpectedFailureTestCase(TestCase):
    """ Unittest supports marking a test as an 'expected failure,' 
        a test that is broken and will fail, but shouldn't be 
        counted as a failure on a TestResult."""
            
    @unittest.expectedFailure
    def test_expectedFailure_decorator(self):
        """ Expected failures use the expectedFailure() decorator """
        self.assertEqual(1, 0, "broken")
    # end def test_expectedFailure_decorator
# end class ExpectedFailureTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
