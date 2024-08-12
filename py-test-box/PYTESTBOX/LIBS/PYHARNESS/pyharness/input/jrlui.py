#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.input.jrlui

@brief Journal test state extraction

@author christophe.roquebert

@date   2018/05/05
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                    import abspath
from pyharness.consts           import DEFAULT_OUTPUT_DIRECTORY
from pyharness.files.jrl        import JrlFile
from pyharness.input.providers  import TestHistoryProvider
from pyharness.input.providers  import TestStateTestProvider
from pyharness.arguments        import KeywordArguments
from os                        import F_OK
from os                        import access
from os.path                   import join
from os.path                   import normpath

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
__JRLSTATE_TO_COMMON_STATE = {
    JrlFile.JrlEntry.STATE_SUCCESS: "success",
    JrlFile.JrlEntry.STATE_FAILURE: "failure",
    JrlFile.JrlEntry.STATE_ERROR:   "error",
    }

class JrlTestProvider(TestHistoryProvider, TestStateTestProvider):
    '''
    Extracts the test history from the Jrl file
    '''


    def getTestHistory(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.TestHistoryProvider.getTestHistory
        '''

        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)

        # Variant may contain non-normalized separators
        pathToJournal = normpath(join(versionRoot, product, variant, target, "Journal.jrl"))
        if (access(pathToJournal, F_OK)):
            journal = JrlFile.create(pathToJournal)
        else:
            journal = None
        # end if

        jrlEntries = (journal is not None) and journal.getAllEntries(testId) or []

        return [(__JRLSTATE_TO_COMMON_STATE.get(jrlEntry.getTestState(), "unknown"),
                 jrlEntry.getTestStartDate(),
                 jrlEntry.getTestStopDate(),
                 jrlEntry.getTestMessage()) for jrlEntry in jrlEntries]
    # end def getTestHistory

    __JRLSTATE_TO_COMMON_STATE = {
        JrlFile.JrlEntry.STATE_SUCCESS: "success",
        JrlFile.JrlEntry.STATE_FAILURE: "failure",
        JrlFile.JrlEntry.STATE_ERROR:   "error",
        }

    def getTestState(self, testId, product, variant, target):
        '''
        @copydoc pyharness.input.providers.TestHistoryProvider.getTestHistory
        '''

        root = abspath(self._kwArgs[KeywordArguments.KEY_ROOT])
        versionRoot = join(root, DEFAULT_OUTPUT_DIRECTORY)

        # Variant may contain non-normalized separators
        pathToJournal = normpath(join(versionRoot, product, variant, target, "Journal.jrl"))
        if (access(pathToJournal, F_OK)):
            journal = JrlFile.create(pathToJournal)
        else:
            journal = None
        # end if

        jrlEntry = (journal is not None) and journal.getLastEntry(testId) or None

        result = "unknown"
        if jrlEntry is not None:
            result = self.__JRLSTATE_TO_COMMON_STATE.get(jrlEntry.getTestState(), "unknown")
        # end if

        return result
    # end def getTestState
# end class JrlTestProvider

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
