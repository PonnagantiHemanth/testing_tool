#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.failure

@brief Auto Test of failures & errors handling and 
                    setUp & tearDown processing

@author christophe.roquebert

@date   2018/09/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------

from pyharness.core import TestCase

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class State(object):
    """
    Singleton
    """
    state = 0

    @staticmethod
    def forward():
        """
        Increase state
        """
        State.state += 3
    # end def forward

    @staticmethod
    def backward():
        """
        Decrease state
        """
        State.state -= 2
    # end def backward
# end class State

class SetUpTearDownTestCase(TestCase):
    """
    SetUp & TearDown processing
    """
    def setUp(self):
        """
        Setup
        """
        State.state = 0
    # end def setUp

    def testForward(self):
        """
        Forward nominal test
        """
        State.forward()
        self.assertEqual(3,
                         State.state,
                         "Invalid state after forward move")
    # end def testForward

    def testBackward(self):
        """Backward nominal test"""
        State.backward()
        self.assertEqual(-2,
                         State.state,
                         "Invalid state after backward move")
    # end def testBackward
# end class SetUpTearDownTestCase


class FailureTestCase(TestCase):
    """
    Failure handling
    """
    def setUp(self):
        """
        FailureTestCase Setup
        """
        super(FailureTestCase, self).setUp()
        
        if self._testMethodName == 'testFailureInSetup':
            self.assertEqual(1, 0, "Force failure during setUp")
        # end if
    # end def setUp
    
    def tearDown(self):
        """
        FailureTestCase tearDown
        """
        if self._testMethodName == 'testFailureInTearDown':
            self.assertEqual(1, 0, "Force failure during tearDown")
        # end if
        
        super(FailureTestCase, self).tearDown()
    # end def tearDown

    def testFailureInSetup(self):
        """
        Failure in SetUp shall trigger an error
        """
        pass
    # end def testFailureInSetup

    def testFailure(self):
        """
        Failure handling
        """
        self.assertEqual(1, 0, "Check failure is caught during test")
    # end def testFailure

    def testFailureInTearDown(self):
        """
        Failure in tearDown shall trigger an error
        """
        pass
    # end def testFailureInTearDown
# end class FailureTestCase


class ErrorTestCase(TestCase):
    """
    Error handling
    """
    def setUp(self):
        """
        ErrorTestCase Setup
        """
        super(ErrorTestCase, self).setUp()
        
        if self._testMethodName == 'testErrorInSetup':
            raise Exception("Force error during setUp")
        # end if
    # end def setUp
    
    def tearDown(self):
        """
        ErrorTestCase tearDown
        """
        if self._testMethodName == 'testErrorInTearDown':
            raise Exception("Force error during tearDown")
        # end if
        
        super(ErrorTestCase, self).tearDown()
    # end def tearDown

    def testErrorInSetup(self):
        """
        Failure in SetUp shall trigger an error
        """
        pass
    # end def testFailureInSetup

    def testError(self):
        """
        Error handling
        """
        raise Exception("Check error is caught during test")
    # end def testError
    
    def testErrorInTearDown(self):
        """
        Error in tearDown shall trigger an error
        """
        pass
    # end def testErrorInTearDown
# end class ErrorTestCase
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
