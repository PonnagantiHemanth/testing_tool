#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.providers

@brief  Base implementation of the test providers

@author christophe.roquebert

@date   2018/05/07
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import abspath
from shutil import rmtree
from unittest import TestCase

from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class TestProviderTestCase(TestCase):
    '''
    Base class for tests of classes derived from TestProvider
    '''

    def setUp(self):
        '''
        Test initialization
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))
    # end def setUp

    def tearDown(self):
        '''
        Test cleanup
        '''
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown


    def _getTestProvider(self):
        '''
        Obtains an instance of the TestProvider
        '''
        raise NotImplementedError
    # end def _getTestProvider
# end class TestProviderTestCase

STATIC_TESTCASE_ID1 = "STATIC_TESTCASE_ID1"
STATIC_TESTCASE_ID2 = "STATIC_TESTCASE_ID2"

class StaticTestCasesProviderTestMixin():
    '''
    Mixin for tests of the StaticTestCasesProvider class

    This assumes that the class under test contains:
    - A test @c mocktest.MockTestCase.test_0WithTestCase implementing the static TestCases STATIC_TESTCASE1 and STATIC_TESTCASE2
    - A test @c mocktest.MockTest.test_1WithoutTestCase that does not implement any TestCases
    - A test @c mocktest.MockTest.test_ThisTestDoesNotExist that does not exist
    '''

    def test_getStaticTestCases_TwoTestCases(self):
        '''
        Test of the getStaticTestCases API, when a testCase is found
        '''
        testId = 'mocktest.MockTest.test_0WithTestCase'
        testProvider = self._getTestProvider()
        obtained = set(testProvider.getStaticTestCases(testId))
        expected = set((STATIC_TESTCASE_ID1, STATIC_TESTCASE_ID2))

        self.assertEqual(expected,
                         obtained,
                         "Invalid TestCases")
    # end def test_getStaticTestCases_TwoTestCases

    def _test_getStaticTestCases_NoTestCases(self):
        '''
        Test of the getStaticTestCases API, when no TestCase is found
        '''
        testId = 'mocktest.MockTest.test_1WithoutTestCase'
        testProvider = self._getTestProvider()
        obtained = set(testProvider.getStaticTestCases(testId))
        expected = set()

        self.assertEqual(expected,
                         obtained,
                         "Invalid TestCases")
    # end def test_getStaticTestCases_NoTestCases

    def _test_getStaticTestCases_NoTest(self):
        '''
        Test of the getStaticTestCases API, when no test is found
        '''
        testId = 'mocktest.MockTest.test_ThisTestDoesNotExist'
        testProvider = self._getTestProvider()
        obtained = set(testProvider.getStaticTestCases(testId))
        expected = set()

        self.assertEqual(expected,
                         obtained,
                         "Invalid TestCases")
    # end def test_getStaticTestCases_NoTest
# end class StaticTestCasesProviderTestMixin

DYNAMIC_TESTCASE_ID1 = "DYNAMIC_TESTCASE_ID1"
DYNAMIC_TESTCASE_ID2 = "DYNAMIC_TESTCASE_ID2"

class DynamicTestCasesProviderTestMixin():
    '''
    Mixin for tests of the DynamicTestCasesProvider class

    This assumes that the repository contains
    - @c mocktest.MockTestCase.test_0WithTestCase, validating DYNAMIC_TESTCASE_ID1
    '''

    @staticmethod
    def getContext():
        '''
        Obtains a mock context

        @return A mock context
        '''
        class MockContext(object):
            '''
            A mock context
            '''

            @staticmethod
            def getCurrentProduct():
                '''
                Obtains a dummy product

                @return a dummy product
                '''
                return 'MOCK_PRODUCT'
            # end def getCurrentProduct

            @staticmethod
            def getCurrentVariant():
                '''
                Obtains a dummy variant

                @return a dummy variant
                '''
                return 'MOCK_VARIANT'
            # end def getCurrentVariant

            @staticmethod
            def getCurrentTarget():
                '''
                Obtains a dummy target

                @return a dummy target
                '''
                return 'MOCK_TARGET'
            # end def getCurrentTarget

            @staticmethod
            def getCurrentMode():
                '''
                Obtains a dummy mode

                @return a dummy mode
                '''
                return 'MOCK_MODE'
            # end def getCurrentMode
        # end class MockContext

        return MockContext()
    # end def getContext


    def test_getDynamicTestCases_TwoTestCases(self):
        '''
        Test of the getDynamicTestCases API, when a TestCase is found
        '''
        testId = 'mocktest.MockTest.test_0WithTestCase'
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()
        obtained = set(testProvider.getDynamicTestCases(testId, product, variant, target))
        expected = set(((DYNAMIC_TESTCASE_ID1, None, None),
                        (DYNAMIC_TESTCASE_ID2, 'user.test', 'This is a comment')))

        self.assertEqual(expected,
                         obtained,
                         "Invalid TestCases")
    # end def test_getDynamicTestCases_TwoTestCases

    def test_getDynamicTestCases_NoTestCases(self):
        '''
        Test of the getDynamicTestCases API, when no TestCase is found
        '''
        testId = 'mocktest.MockTest.test_1WithoutTestCase'
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()
        obtained = set(testProvider.getDynamicTestCases(testId, product, variant, target))
        expected = set()

        self.assertEqual(expected,
                         obtained,
                         "Invalid TestCases")
    # end def test_getDynamicTestCases_NoTestCases

    def test_getDynamicTestCases_NoTest(self):
        '''
        Test of the getDynamicTestCases API, when no test is found
        '''
        testId = 'mocktest.MockTest.test_ThisTestDoesNotExist'
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()
        obtained = set(testProvider.getDynamicTestCases(testId, product, variant, target))
        expected = set()

        self.assertEqual(expected,
                         obtained,
                         "Invalid TestCases")
    # end def test_getDynamicTestCases_NoTest
# end class DynamicTestCasesProviderTestMixin

class TestStateTestProviderTestMixin():
    '''
    Mixin for tests of the TestStateTestProvider class

    This assumes that the repository contains
    - @c mocktest.MockTestCase.test_Success, in success
    - @c mocktest.MockTestCase.test_Failure, in failure
    - @c mocktest.MockTestCase.test_Error, in error
    - @c mocktest.MockTestCase.test_Unknown, unknown
    '''

    IDSTATES = (("success", 'mocktest.MockTest.test_Success'),
                ("failure", 'mocktest.MockTest.test_Failure'),
                ("error", 'mocktest.MockTest.test_Error'),
                ("unknown", 'mocktest.MockTest.test_Unknown'),
                )

    @staticmethod
    def getContext():
        '''
        Obtains a mock context

        @return A mock context
        '''
        class MockContext(object):
            '''
            A mock context
            '''

            @staticmethod
            def getCurrentProduct():
                '''
                Obtains a dummy product

                @return a dummy product
                '''
                return 'MOCK_PRODUCT'
            # end def getCurrentProduct

            @staticmethod
            def getCurrentVariant():
                '''
                Obtains a dummy variant

                @return a dummy variant
                '''
                return 'MOCK_VARIANT'
            # end def getCurrentVariant

            @staticmethod
            def getCurrentTarget():
                '''
                Obtains a dummy target

                @return a dummy target
                '''
                return 'MOCK_TARGET'
            # end def getCurrentTarget

            @staticmethod
            def getCurrentMode():
                '''
                Obtains a dummy mode

                @return a dummy mode
                '''
                return 'MOCK_MODE'
            # end def getCurrentMode
        # end class MockContext

        return MockContext()
    # end def getContext

    def _test_GetTestState_Checked(self, checkedState):
        '''
        Utility function for testing a given state

        @param checkedState [in] (str) The state to check
        '''
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()

        for state, testId in self.IDSTATES:
            obtained = testProvider.getTestState(testId, product, variant, target)

            if (state == checkedState):
                self.assertEqual(checkedState,
                                 obtained,
                                 "Invalid test state")
            else:
                self.assertNotEqual(checkedState,
                                 obtained,
                                 "Invalid test state")
            # end if
        # end for
    # end def _test_GetTestState_Checked

    def test_GetTestState_Success(self):
        '''
        Test of the getTestState API, when the test is in success
        '''
        self._test_GetTestState_Checked("success")
    # end def test_GetTestState_Success


    def test_GetTestState_Error(self):
        '''
        Test of the getTestState API, when the test is in error
        '''
        self._test_GetTestState_Checked("error")
    # end def test_GetTestState_Error

    def test_GetTestState_Failure(self):
        '''
        Test of the getTestState API, when the test is in failure
        '''
        self._test_GetTestState_Checked("failure")
    # end def test_GetTestState_Failure

    def test_GetTestState_Unknown(self):
        '''
        Test of the getTestState API, when the test is unknown
        '''
        self._test_GetTestState_Checked("unknown")
    # end def test_GetTestState_Unknown
# end class TestStateTestProviderTestMixin

class PerfDataTestProviderTestMixin():
    '''
    Mixin for tests of PerfDataTestProvider class

    This assumes that the repository contains
    - @c mocktest.MockTestCase.test_PerfData0, contains no perf data
    - @c mocktest.MockTestCase.test_PerfData1, contains PERF_1 1 s
    - @c mocktest.MockTestCase.test_PerfDataNone does not exist
    '''


    def test_PerfDataOnePerfData(self):
        '''
        Test of the getPerfData API, when the test contains one performance data
        '''
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()

        obtained = testProvider.getPerfData('mocktest.MockTestCase.test_PerfData1', product, variant, target)
        expected = {'PERF_1': [(1, 's')]}
        self.assertEqual(expected,
                         obtained,
                         "Invalid perfdata")
    # end def test_PerfDataOnePerfData

    def test_PerfDataNoPerfData(self):
        '''
        Test of the getPerfData API, when the test does not contain any
        '''
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()

        obtained = testProvider.getPerfData("mocktest.MockTestCase.test_PerfData0", product, variant, target)
        expected = []
        self.assertEqual(expected,
                         obtained,
                         "Invalid perfdata")
    # end def test_PerfDataNoPerfData

    def test_PerfDataNoTest(self):
        '''
        Test of the getPerfData API, when the test does not contain any
        '''
        testProvider = self._getTestProvider()
        product = self.getContext().getCurrentProduct()
        variant = self.getContext().getCurrentVariant()
        target  = self.getContext().getCurrentTarget()

        obtained = testProvider.getPerfData("mocktest.MockTestCase.test_PerfDataNone", product, variant, target)
        expected = []
        self.assertEqual(expected,
                         obtained,
                         "Invalid perfdata")
    # end def test_PerfDataNoTest
# end class PerfDataTestProviderTestMixin

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
