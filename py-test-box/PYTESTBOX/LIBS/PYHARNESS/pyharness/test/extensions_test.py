#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.extensionstest

@brief PyHarnessCase test implementation

This module contains the test cases for the PyHarnessCase class.

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core                      import TestException
from pyharness.extensions                import PyHarnessCase
from pyharness.test.core_test             import MockContext
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class PyHarnessCaseTestCase( TestCase ):                                                                                 # pylint:disable=R0901
    '''
    Tests the PyHarnessCase class
    '''

    def _test_assertBug(self, bug, checkIfBug, checkIfNotBug, message, failIfException):
        '''
        Builds a sub-environment, asserting for a bug, and checking the result.

        @param bug             [in] (bool) The bug parameter to check
        @param checkIfBug      [in] (bool) Whether the bug presence should be checked
        @param checkIfNotBug   [in] (bool) Whether the bug absence should be checked
        @param message         [in] (str) The error message
        @param failIfException [in] (bool) What should be tested
        '''

        collector = [None]
        class BugTestCase(PyHarnessCase):                                                                                #pylint:disable=R0901
            '''
            Class containing the actual test
            '''
            def testMe(self):
                '''
                The actual test method.
                '''
                collector[0] = False
                try:
                    self.assertBug(bug, checkIfBug, checkIfNotBug, message)
                    collector[0] = not failIfException
                except TestException:
                    if failIfException is None:
                        raise
                    else:
                        collector[0] = failIfException
                    # end if
                except Exception:
                    if failIfException is not None:
                        raise
                    # end if
                # end try
            # end def testMe
        # end class BugTestCase

        result = None
        context = MockContext()

        testCase = BugTestCase('testMe')
        testCase.run(result, context)

        self.assertTrue(collector[0] is not None,
                        'Error in test')
        self.assertFalse(collector[0],
                         message)
    # end def _test_assertBug

    def test_assertBug_Bug_Found(self):
        '''
        Tests the assertBug method when:
        - A bug should be found
        - A bug _is_ found
        '''
        bug           = True
        checkIfBug    = True
        checkIfNotBug = False

        self._test_assertBug(bug, checkIfBug, checkIfNotBug, message = "Bug triggered when not present", failIfException = True)
    # end def test_assertBug_Bug_Found

    def test_assertBug_Bug_NotFound(self):
        '''
        Tests the assertBug method when:
        - A bug should be found
        - A bug _is_not_ found
        '''
        bug           = True
        checkIfBug    = False
        checkIfNotBug = True

        self._test_assertBug(bug, checkIfBug, checkIfNotBug, message = "Bug not triggered when not present", failIfException = False)
    # end def test_assertBug_Bug_NotFound

    def test_assertBug_NoBug_Found(self):
        '''
        Tests the assertBug method when:
        - A bug should be found
        - A bug _is_not_ found
        '''
        bug           = False
        checkIfBug    = True
        checkIfNotBug = False

        self._test_assertBug(bug, checkIfBug, checkIfNotBug, message = "Bug not triggered when present", failIfException = False)
    # end def test_assertBug_NoBug_Found

    def test_assertBug_NoBug_NotFound(self):
        '''
        Tests the assertBug method when:
        - A bug should be found
        - A bug _is_not_ found
        '''
        bug           = False
        checkIfBug    = False
        checkIfNotBug = True

        self._test_assertBug(bug, checkIfBug, checkIfNotBug, message = "Bug found when not present", failIfException = True)
    # end def test_assertBug_NoBug_NotFound

    def test_assertBug_Inconsistency(self):
        '''
        Tests the assertBug method when a bug is both found and not found
        - A bug should be found
        - A bug _is_not_ found
        '''
        bug           = False
        checkIfBug    = True
        checkIfNotBug = True

        self._test_assertBug(bug, checkIfBug, checkIfNotBug, message = "Bug found when not present", failIfException = None)

        bug           = False
        checkIfBug    = False
        checkIfNotBug = False

        self._test_assertBug(bug, checkIfBug, checkIfNotBug, message = "Bug found when not present", failIfException = None)
        # end try

    # end def test_assertBug_Inconsistency
# end class PyHarnessCaseTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
