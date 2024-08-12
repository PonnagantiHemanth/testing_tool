#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.test.jrltest

@brief Tests of the JrlTestProvider

@author christophe.roquebert

@date   2018/05/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.consts                   import DEFAULT_OUTPUT_DIRECTORY
from pyharness.input.jrlui              import JrlTestProvider
from pyharness.input.test.providers_test     import TestProviderTestCase
from pyharness.input.test.providers_test     import TestStateTestProviderTestMixin
from pyharness.arguments                import KeywordArguments
from os                                import makedirs
from os.path                           import join
from os.path                           import normpath

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

MOCK_JRL_BODY = '\n'.join(("",
                           "mocktest.MockTest.test_Success 2006-01-01 00:00:00 2006-01-01 00:00:01 Failed Failure message",
                           "mocktest.MockTest.test_Success 2006-01-01 00:00:00 2006-01-01 00:00:01 Ok",
                           "mocktest.MockTest.test_Failure 2006-01-01 00:00:00 2006-01-01 00:00:01 Ok",
                           "mocktest.MockTest.test_Failure 2006-01-01 00:00:00 2006-01-01 00:00:01 Failed Failure message",
                           "mocktest.MockTest.test_Error   2006-01-01 00:00:00 2006-01-01 00:00:01 Ok",
                           "mocktest.MockTest.test_Error   2006-01-01 00:00:00 2006-01-01 00:00:01 Error Error message",
                           ))
class JrlTestProviderTestCase(TestStateTestProviderTestMixin,
                              TestProviderTestCase):
    '''
    Tests of the JrlTestProviderTestCase
    '''

    def setUp(self):
        '''
        Test initialization
        '''
        TestProviderTestCase.setUp(self)

        jrlFilePathElements = [self._tempDirPath,
                               DEFAULT_OUTPUT_DIRECTORY,
                               self.getContext().getCurrentProduct(),
                               self.getContext().getCurrentVariant(),
                               self.getContext().getCurrentTarget()]

        jrlFilePath = normpath(join(*jrlFilePathElements))
        makedirs(jrlFilePath)
        with open(join(jrlFilePath, 'Journal.jrl'), "w+") as jrlFile:
            jrlFile.write(MOCK_JRL_BODY)
        # end with
    # end def setUp

    def _getTestProvider(self):
        '''
        @copydoc pyharness.input.test.providers.TestProviderTestCase._getTestProvider
        '''
        # The root is obtained from the current file
        kwArgs = {}
        kwArgs.update(KeywordArguments.DEFAULT_ARGUMENTS)
        kwArgs[KeywordArguments.KEY_ROOT] = self._tempDirPath

        return JrlTestProvider(kwArgs)
    # end def _getTestProvider

# end class JrlTestProviderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
