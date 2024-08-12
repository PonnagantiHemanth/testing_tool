#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.deprecation

@brief  Deprecation warnings testing module

        The stderr in python level is not low leveled enough to catch the @c c warning.
        We can't check easily the deprecated warning and its ignorance but we can
        run the test and check that no exception is raised

@author christophe Roquebert

@date   2018/02/14
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from io                          import StringIO
from pylibrary.tools.deprecation       import deprecated
from pylibrary.tools.deprecation       import ignoredeprecation
from unittest                           import TestCase
import sys

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class IgnoreDeprecationWarningTestCase(TestCase):
    '''
    Tests the behavior of the IgnoreWarning class
    '''

    def setUp(self):
        '''
        Constructor
        '''
        super(IgnoreDeprecationWarningTestCase, self).setUp()

        self.backupStderr = sys.stderr
        sys.stderr.flush()
        sys.stderr = StringIO()

    # end def setUp

    def tearDown(self):
        '''
        TearDown of IgnoreWarning tests
        '''
        sys.stderr.close()
        sys.stderr = self.backupStderr
        super(IgnoreDeprecationWarningTestCase, self).tearDown()
    # end def tearDown

    @staticmethod
    def checkWarningPresent(warning):
        '''
        Check warning as been catch

        @param  warning [in] (string) Check the warning
        '''
        pass
    # end def checkWarningPresent

    @staticmethod
    def checkWarningNotPresent():
        '''
        Check no warning as been catch
        '''
        pass
    # end def checkWarningNotPresent

    def testIgnoredeprecation(self):
        '''
        Tests ignoredeprecation method
        '''
        @deprecated
        def deprecatedMethod():
            '''
            Deprecated method
            '''
            pass
        # end def deprecatedMethod

        @ignoredeprecation
        def deprecationToIgnore():
            '''
            Call a deprecated method
            '''
            deprecatedMethod()                                                                                          #pylint:disable=W8301
        # end def deprecationToIgnore

        deprecationToIgnore()
        self.checkWarningNotPresent()

    # end def testIgnoredeprecation

    def testDeprecatedProperty(self):
        '''
        Tests deprecated defined as property
        '''
        class TestClass(object):
            '''
            Testing class
            '''
            RESULT  = 0
            def __init__(self):
                '''
                Constructor
                '''
                super(TestClass, self).__init__()

                self.value = None
            # end def __init__

            def getUpdated(self):
                '''
                Reference method

                @return (int) 0
                '''
                return self.RESULT
            # end def getUpdated

            def setUpdated(self, value):
                '''
                Reference method

                @param  value [in] (int) Unused value
                '''
                self.value = value
            # end def setUpdated

            updated = property(getUpdated, setUpdated)

            deprecatedProperty = deprecated(updated, 'Use updated instead')
        # end class TestClass

        testClass = TestClass()

        obtained = testClass.deprecatedProperty

        self.assertEqual(TestClass.RESULT,
                         obtained,
                         'Wrong result returned')

        self.checkWarningPresent('Use updated instead')

        expected = 2

        testClass.deprecatedProperty = expected

        self.assertEqual(expected,
                         testClass.value,
                         'Wrong result returned')

        self.checkWarningPresent('Use updated instead')

    # end def testDeprecatedProperty

    def testDeprecatedDeadline(self):
        '''
        Tests a deprecated method with deadline
        '''
        class TestClass(object):
            '''
            Testing class
            '''
            RESULT = 0

            def getUpdated(self):
                '''
                Reference method

                @return (int) 0
                '''
                return self.RESULT
            # end def getUpdated

            def setUpdated(self, unusedValue):
                '''
                Reference method

                @param  unusedValue [in] (int) Unused value
                '''
                pass
            # end def setUpdated

            @deprecated('Deprecated method with old deadline', deadline = '2000/01/01')
            def deprecatedMethod(self):
                '''
                Deprecated method
                '''
                pass
            # end def deprecatedMethod

            updated = property(getUpdated, setUpdated)

            deprecatedProperty = deprecated(updated, 'Use updated instead', deadline = '2000/01/01')
        # end class TestClass

        testClass = TestClass()

        self.assertRaises(DeprecationWarning,
                          testClass.deprecatedMethod)

        self.assertRaises(DeprecationWarning,
                          lambda: testClass.deprecatedProperty)

        self.assertRaises(DeprecationWarning,
                          testClass.__setattr__,
                          'deprecatedProperty', 1)

    # end def testDeprecatedDeadline

# end class IgnoreDeprecationWarningTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
