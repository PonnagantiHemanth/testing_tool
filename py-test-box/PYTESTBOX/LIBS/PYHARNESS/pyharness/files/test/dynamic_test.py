#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.files.test.dynamic

@brief  Tests of the DynamicFile class

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.core import TestCase as CoreTestCase
from pyharness.files.dynamic import DynamicFile
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
TEST_TESTCASE_1 = "TEST_TESTCASE_1"
TEST_TESTCASE_2 = "TEST_TESTCASE_2"


class DynamicFileTestCase(TestCase):                                                                                    # pylint:disable=R0901
    '''
    Tests the DynamicFile class.
    '''

    TestedClass = DynamicFile

    def _createInstance(self, dynamicPath = None):
        '''
        Create an instance of DynamicFile

        @option dynamicPath [in] (str) Path to the TESTCASES/dynamic file

        @return (DynamicFile) DynamicFile instance
        '''
        if (dynamicPath is None):
            dynamicPath = join(self.__tempDirPath, "dynamic")
        # end if

        return self.TestedClass(dynamicPath)
    # end def _createInstance

    class MockTestCase(CoreTestCase):
        '''
        The test case to check
        '''
        def runTest(self):
            '''
            Stub
            '''
            pass
        # end def runTest
    # end class MockTestCase

    def setUp(self):
        '''
        Initialize test.
        '''
        TestCase.setUp(self)

        # Create a fake test cases file
        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        '''
        Cleanup test.
        '''
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def testLoad(self):
        '''
        Tests testcases file load
        '''
        # Create a fake test cases file
        path = join(self.__tempDirPath, "dynamic")
        with open(path, "w+") as tempFile:
            tempFile.write("|test1\n crit1\n crit2||user.test||comment")
        # end with

        dynamicFile = self._createInstance(path)
        dynamicFile.load()
        self.assertEqual(["test1"],
                         list(dynamicFile._testcases.keys()),                                                           # pylint:disable=W0212
                         "Invalid loaded keys")
        self.assertEqual(set([("crit1", None, None), ("crit2", "user.test", "comment")]),
                         dynamicFile._testcases["test1"],                                                               # pylint:disable=W0212
                         "Invalid loaded test cases")
    # end def testLoad

    def testSave(self):
        '''
        Validates testcases
        '''
        testCase = self.MockTestCase()

        testCase.testCaseChecked(TEST_TESTCASE_1)
        testCase.testCaseChecked(TEST_TESTCASE_2)

    # end def testSave

    class MockContext(object):
        '''
        A mock context
        '''
        kill = False
        abort = False

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

        @staticmethod
        def filter(testCase, context):                                                                                  #@ReservedAssignment pylint:disable=W0613
            '''
            Dummy filter

            @param  testCase [in] (TestCase) The current test case
            @param  context  [in] (Context) The context to filter

            @return (boolean) True
            '''
            return True
        # end def filter

        @staticmethod
        def collectOnly():
            '''
            Stub

            @return collection state (never collect)
            '''
            return False
        # end def collectOnly

        def getParent(self):
            '''
            Obtains mock parent

            @return mock parent
            '''
            return self
        # end def getParent
    # end class MockContext

    def testSaveTwice(self):
        '''
        Validates a test case
        '''

        collector = []
        class StubTestCase(CoreTestCase):
            '''
            A stubbed test case
            '''

            def _innerCall(self):
                '''
                An inner call.
                '''
                self.testCaseChecked(TEST_TESTCASE_1)
            # end def _innerCall

            def testMe(self):
                '''
                The test entry
                '''
                self.testCaseChecked(TEST_TESTCASE_1)
                try:
                    self.testCaseChecked(TEST_TESTCASE_1)
                except AssertionError:
                    collector.append(True)
                # end try
            # end def testMe
        # end class StubTestCase

        testCase = StubTestCase('testMe')
        result = None
        context = self.MockContext()
        testCase.run(result  = result,
                     context = context)

        self.assertTrue(any(collector),
                        'No exception raised when testCaseChecked is called twice')
    # end def testSaveTwice

    def testSaveFromInner(self):
        '''
        Validates a testcase from outside the test
        '''

        collector = []
        class StubTestCase(CoreTestCase):
            '''
            A stubbed test case
            '''

            def _innerCall(self):
                '''
                An inner call.
                '''
                self.testCaseChecked(TEST_TESTCASE_1)
            # end def _innerCall

            def testMe(self):
                '''
                The test entry
                '''
                try:
                    self._innerCall()
                except AssertionError:
                    collector.append(True)
                # end try
            # end def testMe
        # end class StubTestCase

        testCase = StubTestCase('testMe')
        result = None
        context = self.MockContext()
        testCase.run(result  = result,
                     context = context)

        self.assertTrue(any(collector),
                        'No exception raised when testCaseChecked is NOT in a top-level test method')
    # end def testSaveFromInner

    def testAddTestCase(self):
        '''
        Tests addTestCase method
        '''
        testId      = 'testId'
        testcase    = 'TESTCASE'
        author      = 'user'
        comment     = 'this is a comment'
        dynamicFile = self._createInstance()

        dynamicFile.addTestCase(testId, testcase, author, comment)
        self.assertEqual(set([(testcase, author, comment)]),
                         dynamicFile.getTestCases(testId),
                         'Wrong Test cases added')

    # end def testAddTestCase

    def testRemoveTestCase(self):
        '''
        Tests removeTestCase method
        '''
        testId      = 'testId'
        testcase1   = 'TESTCASE1'
        testcase2   = 'TESTCASE2'
        testcase3   = 'TESTCASE3'
        author      = 'user'
        comment     = 'this is a comment'
        dynamicFile = self._createInstance()

        dynamicFile.addTestCase(testId, testcase1, author, comment)
        dynamicFile.addTestCase(testId, testcase2, author, comment)
        dynamicFile.addTestCase(testId, testcase3, author, comment)

        dynamicFile.removeTestCases(testId)

        self.assertEqual(set(),
                         dynamicFile.getTestCases(testId),
                         'Wrong Test cases added')

    # end def testRemoveTestCase

    def testSaveCreate(self):
        '''
        Tests save and create methods
        '''
        testId      = 'testId'
        testcase1   = 'TESTCASE1'
        testcase2   = 'TESTCASE2'
        author      = 'user'
        comment     = 'this is a comment'
        dynamicFile = self._createInstance()

        dynamicFile.addTestCase(testId, testcase1)
        dynamicFile.addTestCase(testId, testcase2, author, comment)

        dynamicFile.save()
        dynamicFile2 = self.TestedClass.create(dynamicFile._dynamicPath)                                                #pylint:disable=W0212

        self.assertEqual(dynamicFile.getTestCases(testId),
                         dynamicFile2.getTestCases(testId),
                         'Wrong testcases saving')

        dynamicFile2 = self.TestedClass.create(dynamicFile._dynamicPath, True)                                          #pylint:disable=W0212

        self.assertEqual(set([]),
                         dynamicFile2.getTestCases(testId),
                         'Wrong testcases saving')

    # end def testSaveCreate

# end class DynamicFileTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
