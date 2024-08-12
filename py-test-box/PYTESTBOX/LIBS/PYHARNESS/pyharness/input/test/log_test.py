#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.logtest

@brief  Tests of the LogTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.consts                   import DEFAULT_OUTPUT_DIRECTORY
from pyharness.input.test.providers_test     import DynamicTestCasesProviderTestMixin
from pyharness.input.test.providers_test     import TestProviderTestCase
from pyharness.input.test.providers_test     import TestStateTestProviderTestMixin
from pyharness.input.logui              import LogTestProvider
from pyharness.arguments                import KeywordArguments
from os                                import makedirs
from os.path                           import join
from os.path                           import normpath
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

MOCK_LOG_SUCCESS_BODY = '\n'.join(('',
                                   r'# Title2:   mocktest.MockTest.test_Success --> Ok',
                                   ''))

MOCK_LOG_FAILURE_BODY = '\n'.join(('',
                                   r'# Title2:   mocktest.MockTest.test_Failure --> Fail',
                                   ''))

MOCK_LOG_ERROR_BODY = '\n'.join(('',
                                   r'# Title2:   mocktest.MockTest.test_Error --> Error',
                                   ''))

MOCK_LOG_TESTCASE_BODY = '\n'.join(('',
                                    r'# TestCase: DYNAMIC_TESTCASE_ID1',
                                    r'# TestCase: DYNAMIC_TESTCASE_ID2 user.test (This is a comment)',
                                    ))

MOCK_LOG_NOTESTCASE_BODY = '\n'.join(('',
                                     ))


LOG_FILES = (('mocktest.MockTest.test_Success', MOCK_LOG_SUCCESS_BODY),
             ('mocktest.MockTest.test_Failure', MOCK_LOG_FAILURE_BODY),
             ('mocktest.MockTest.test_Error', MOCK_LOG_ERROR_BODY),
             ('mocktest.MockTest.test_0WithTestCase', MOCK_LOG_TESTCASE_BODY),
             ('mocktest.MockTest.test_1WithoutTestCase', MOCK_LOG_NOTESTCASE_BODY)
             )

class LogTestProviderTestCase(DynamicTestCasesProviderTestMixin,
                              TestStateTestProviderTestMixin,
                              TestProviderTestCase):
    '''
    Tests of the LogTestProvider
    '''

    def setUp(self):
        '''
        Test initialization
        '''
        TestProviderTestCase.setUp(self)

        logFilePathElements = [self._tempDirPath,
                               DEFAULT_OUTPUT_DIRECTORY,
                               self.getContext().getCurrentProduct(),
                               self.getContext().getCurrentVariant(),
                               self.getContext().getCurrentTarget(),
                               "log"]

        logFilePath = normpath(join(*logFilePathElements))
        makedirs(logFilePath)
        for testId, body in LOG_FILES:
            with open(join(logFilePath, '%s.log' % testId), "w+") as logFile:
                logFile.write(body)
            # end with
        # end for
    # end def setUp

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        kwArgs = {}
        kwArgs.update(KeywordArguments.DEFAULT_ARGUMENTS)
        kwArgs[KeywordArguments.KEY_ROOT] = self._tempDirPath

        return LogTestProvider(kwArgs)
    # end def _getTestProvider

# end class LogTestProviderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
