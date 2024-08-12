#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.logui

@brief Providers for the LogTestListener

@author christophe.roquebert

@date   2018/05/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                    import abspath
from pyharness.consts           import DEFAULT_OUTPUT_DIRECTORY
from pyharness.input.providers  import DynamicTestCasesProvider
from pyharness.input.providers  import TestStateTestProvider
from pyharness.arguments        import KeywordArguments
from os                         import F_OK
from os                         import access
from os.path                    import join
from os.path                    import normpath
import re

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LogTestProvider(TestStateTestProvider, DynamicTestCasesProvider):
    '''
    Providers for the LogTestListener class
    '''

    TESTCASE_PATTERN = re.compile('.*TestCase: ([^\\s]+)(?:\\s([^\\s]+)?)?(?:\\s+\\((.*)\\))?$')
    RESULT_PATTERN   = re.compile('.*Title[1-3]:\\s+[^\\s]+\\s*-->\\s*(.*)\\s*$')

    __MESSAGE_TO_STATE = {"Ok": "success",
                          "Fail": "failure",
                          "Error": "error",
                          }

    def _parseLogContents(self, contents):
        '''
        Extracts information from the contents of a log file

        @param  contents [in] (str) The contents of a log file

        @return A tuple containing the information extracted from a log file
        '''
        dynamicTestCases = []
        state = "unknown"
        for line in [v.strip() for v in contents.split('\n')]:

            # Check for a TestCase
            re_match = self.TESTCASE_PATTERN.match(line)
            if (re_match is not None):
                groups = re_match.groups()
                if len(groups) == 1:
                    dynamicTestCases.append((groups[0], None, None))
                else:
                    dynamicTestCases.append((groups[0], groups[1], groups[2]))
                # end if
            else:
                re_match = self.RESULT_PATTERN.match(line)
                if (re_match is not None):
                    state = self.__MESSAGE_TO_STATE.get(re_match.groups()[0], "unknown")
                # end if
            # end if
        # end for
        return (state, dynamicTestCases)
    # end def _parseLogContents

    def _extractLogContents(self, testId, product, variant, target):
        '''
        Extracts the log contents

        @param  testId  [in] (str) The testId for which to retrieve the contents
        @param  product [in] (str) The product to obtain the contents from
        @param  variant [in] (str) The variant to obtain the contents from
        @param  target  [in] (str) The target to obtain the contents from

        @return The contents, as a str
        '''
        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)
        pathToLog = normpath(join(versionRoot, product, variant, target, "log", "%s.log" % (testId,)))
        if (access(pathToLog, F_OK)):
            with open(pathToLog, "r") as inputFile:
                contents = inputFile.read()
            # end with
        else:
            contents = ""
        # end if

        return contents
    # end def _extractLogContents


    def getDynamicTestCases(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.DynamicTestCasesProvider.getDynamicTestCases
        '''
        contents = self._extractLogContents(testId, product, variant, target)
        results = self._parseLogContents(contents)[1]
        return results
    # end def getDynamicTestCases

    def getTestState(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.TestStateTestProvider.getTestState
        '''
        contents = self._extractLogContents(testId, product, variant, target)
        results = self._parseLogContents(contents)[0]
        return results
    # end def getTestState
# end class LogTestProvider

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
