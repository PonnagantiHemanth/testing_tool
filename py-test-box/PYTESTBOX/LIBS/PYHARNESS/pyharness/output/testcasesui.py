#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.testcasesui

@brief  TestCases file TestListener

@author christophe.roquebert

@date   2018/12/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                            import abspath
from pylibrary.tools.threadutils        import synchronized
from pyharness.arguments                import KeywordArguments
from pyharness.core                     import TestListener
from pyharness.core                     import TestSuite
from pyharness.files.dynamic            import DynamicFile
from os                                 import F_OK
from os                                 import access
from os                                 import makedirs
from os.path                            import join
from threading                          import RLock

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class DynamicTestListener(TestListener):
    '''
    A test listener class that can print formatted text results to a file.

    The file format follows the format defined by ValidVB.
    '''

    RELATIVE_PATH  = "TESTCASES"
    FILE_NAME      = "testcases.dynamic"
    SYNCHRONIZATION_LOCK = RLock()

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        Constructor.

        @copydoc pyharness.core.TestListener.__init__

        At the lowest setting, only the test id is printed.
        At higher settings, a complete test description is printed.
        '''
        super(DynamicTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        self._testCasesFile       = None
    # end def __init__

    def __resultDirPath(self):
        '''
        Builds the path to the directory containing the log files

        @return The file path to the test log.
        '''
        result = abspath(join(self.outputdir, self.RELATIVE_PATH))

        return result
    # end def __resultDirPath

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun

        Empties if needed all log files
        '''
        # Create the dynamic file
        testCasesDir = self.__resultDirPath()
        if (not access(testCasesDir, F_OK)):
            makedirs(testCasesDir)
        # end if


        if (not resumed):
            testCasesPath  = join(testCasesDir, self.FILE_NAME)
            self._testCasesFile = DynamicFile(testCasesPath)

            if (self.args[KeywordArguments.KEY_ERASELOGS]):
                self._testCasesFile.save()
            else:
                self._testCasesFile.load()
            # end if
        # end if
    # end def startRun

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def resetTest(self, test, context):                                                                                 # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.resetTest
        '''
        testCasesDir = self.__resultDirPath()
        if (access(testCasesDir, F_OK)):
            testCasesPath  = join(testCasesDir, self.FILE_NAME)
            self._testCasesFile = DynamicFile(testCasesPath)

            testId = test.id()

            self._testCasesFile.load()
            self._testCasesFile.removeTestCases(testId)
            self._testCasesFile.save()
        # end if
    # end def resetTest

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        if (not isinstance(test, TestSuite)):
            # Should lock the file, until it is released.
            testId = test.id()
            self._testCasesFile.removeTestCases(testId)
            self._testCasesFile.save()
        # end if
    # end def startTest

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addTestCase(self, test, testCase, author=None, comment=None):
        '''
        @copydoc pyharness.core.TestListener.addTestCase

        This registers the testcase in the dynamic file
        '''
        testId = test.id()
        self._testCasesFile.addTestCase(testId,
                                        testCase,
                                        author,
                                        comment)
        self._testCasesFile.save()
    # end def addTestCase
# end class DynamicTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
