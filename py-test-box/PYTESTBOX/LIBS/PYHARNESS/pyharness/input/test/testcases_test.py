#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.testcasestest

@brief Tests of the TestCasesTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.consts                     import DEFAULT_OUTPUT_DIRECTORY
from pyharness.input.testcasesui          import TestCasesTestProvider
from pyharness.input.test.providers_test       import DynamicTestCasesProviderTestMixin
from pyharness.input.test.providers_test       import StaticTestCasesProviderTestMixin
from pyharness.input.test.providers_test       import TestProviderTestCase
from pyharness.arguments                  import KeywordArguments
from os                                  import makedirs
from os.path                             import join
from os.path                             import normpath
from sys                                 import path

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

MOCK_TEST_BODY = '\n'.join(("# -*- coding: utf-8 -*-",
                            "from pyharness.core import TestCase",
                            "from testcases import *",
                            "class MockTest(TestCase):",
                            "    def test_0WithTestCase(self):",
                            "        self.testCaseChecked(STATIC_TESTCASE_ID1)",
                            "        self.testCaseChecked(STATIC_TESTCASE_ID2)",
                            "    # end def test_0WithTestCase",
                            "",
                            "    def test_1WithoutTestCase(self):",
                            "        pass",
                            "    # end def test_1WithoutTestCase",
                            ""))

MOCK_TESTCASES_BODY = '\n'.join(("",
                                 "STATIC_TESTCASE_ID1 = 'STATIC_TESTCASE_ID1'",
                                 "STATIC_TESTCASE_ID2 = 'STATIC_TESTCASE_ID2'",
                                 ""))

MOCK_DYNAMIC_BODY = '\n'.join(("",
                               "|mocktest.MockTest.test_0WithTestCase",
                               " DYNAMIC_TESTCASE_ID1",
                               " DYNAMIC_TESTCASE_ID2||user.test||This is a comment",
                               "",
                               "|mocktest.MockTest.test_1WithoutTestCase",
                               "",
                               ))

class TestCasesTestProviderTest(StaticTestCasesProviderTestMixin,
                                DynamicTestCasesProviderTestMixin,
                                TestProviderTestCase):
    '''
    Tests of the TestCasesTestProvider class
    '''

    def setUp(self):
        '''
        Test initialization
        '''
        super(TestCasesTestProviderTest, self).setUp()

        with open(join(self._tempDirPath, 'mocktest.py'), "w+") as testFile:
            testFile.write(MOCK_TEST_BODY)
        # end with

        with open(join(self._tempDirPath, 'testcases.py'), "w") as testCasesFile:
            testCasesFile.write(MOCK_TESTCASES_BODY)
        # end with

        dynamicFilePathElements = [self._tempDirPath,
                                   DEFAULT_OUTPUT_DIRECTORY,
                                   self.getContext().getCurrentProduct(),
                                   self.getContext().getCurrentVariant(),
                                   self.getContext().getCurrentTarget(),
                                   'TESTCASES']

        dynamicFilePath = normpath(join(*dynamicFilePathElements))
        makedirs(dynamicFilePath)
        with open(join(dynamicFilePath, 'dynamic'), "w+") as dynamicFile:
            dynamicFile.write(MOCK_DYNAMIC_BODY)
        # end with

        path.insert(0, self._tempDirPath)
    # end def setUp

    def tearDown(self):
        '''
        Test cleanup
        '''
        path.remove(self._tempDirPath)

        super(TestCasesTestProviderTest, self).tearDown()
    # end def tearDown

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        # The root is obtained from the current file
        kwArgs = {}
        kwArgs.update(KeywordArguments.DEFAULT_ARGUMENTS)
        kwArgs[KeywordArguments.KEY_ROOT] = self._tempDirPath

        return TestCasesTestProvider(kwArgs)
    # end def _getTestProvider
# end class TestCasesTestProviderTest

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
