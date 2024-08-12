#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.jrlui

@brief  JRL-specialized TestListener

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
from pyharness.files.jrl                import JrlFile
from os                                 import F_OK
from os                                 import R_OK
from os                                 import access
from os                                 import makedirs
from os.path                            import join
from threading                          import RLock
from time                               import localtime

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class JrlTestListener(TestListener):
    '''
    A test listener class that prints the results of a run in the .jrl file.

    This was formerly placed within the LogTestListener, but was moved in a
    separate class separated for the sake of clarity and modularity:
    It is now possible to log to a Jrl file without requiring a Log output.

    Note: The JRL testlistener is less efficient that the previous
          implementation, that simply appended its result to the jrl file.

          This is because the JRL needs to be multithread-compatible, and
          multiple threads may finish their respective tests out of sequence.
    '''

    SYNCHRONIZATION_LOCK = RLock()

    ## This TestListener is one of the few mandatory listeners
    MANDATORY = True
    VISIBLE   = False

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        Constructor.

        @copydoc pyharness.core.TestListener.__init__
        '''
        super(JrlTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        outputDir = self.__resultDirPath()
        if (not access(outputDir, F_OK)):
            makedirs(outputDir)
        # end if

        self._jrlPath = join(outputDir, 'Journal.jrl')
        self._jrlFile = None
    # end def __init__

    def __resultDirPath(self):
        '''
        Builds the path to the directory containing the log files

        @return (str) The file path to the test log.
        '''
        result = abspath(self.outputdir)

        return result
    # end def __resultDirPath

    def getJrlDirPath(self):
        '''
        Get the directory to JRL file

        @return (unicode) Path to JRL file
        '''
        return self.__resultDirPath()
    # end def getJrlDirPath

    def _getJrlFile(self, create=False):
        '''
        Obtains the jrl File, or creates it if needed

        @option create [in] (bool) Whether to re-initialize the file

        @return The JrlFile instance
        '''
        if (self._jrlFile is None):
            if (not access(self._jrlPath, R_OK)):
                open(self._jrlPath, "w").close()
            # end if

            self._jrlFile = JrlFile.create(self._jrlPath, create)
        # end if

        return self._jrlFile
    # end def _getJrlFile

    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun

        Clear if needed the log file.
        Only internal cache is cleared.
        '''
        reInit = (    (not resumed)
                  and (self.args[KeywordArguments.KEY_ERASELOGS]))
        jrlFile = self._getJrlFile(reInit)

        if (not resumed):
            jrlFile.addRunStartComment()
        # end if

    # end def startRun

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        if (not isinstance(test, TestSuite)):

            # Create a new entry for this test
            testId = test.id()
            jrlFile = self._getJrlFile()
            jrlFile.createEntry(testId, localtime())
            jrlFile.save()
        # end if
    # end def startTest

    def resetTest(self, test, context):                                                                                 # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.resetTest
        '''
        if (not isinstance(test, TestSuite)):

            # Create a new entry for this test
            testId = test.id()
            jrlFile = self._getJrlFile()
            faketime = 0
            jrlFile.createEntry(testId, faketime).setTestStopDate(faketime)
            jrlFile.save()
        # end if
    # end def resetTest

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def stopTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.stopTest
        '''
        if (not isinstance(test, TestSuite)):

            testId = test.id()

            jrlFile = self._getJrlFile()
            jrlEntry = jrlFile.getLastEntry(testId)
            jrlEntry.setTestStopDate(localtime())

            jrlFile.save()
        # end if
    # end def stopTest

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addFailure(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addFailure
        '''

        if (not isinstance(test, TestSuite)):

            testId = test.id()

            jrlFile = self._getJrlFile()
            jrlEntry = jrlFile.getLastEntry(testId)
            jrlEntry.setTestState('Failed')

            excp = err[1]
            message = str(excp.args[0]) if len(excp.args) == 1 else ''
            message = message.split("\n", 1)[0].strip()
            jrlEntry.setTestMessage(message)

            jrlFile.save()
        # end if
    # end def addFailure

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addError(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addError
        '''

        if (not isinstance(test, TestSuite)):

            testId = test.id()

            jrlFile = self._getJrlFile()
            jrlEntry = jrlFile.getLastEntry(testId)
            jrlEntry.setTestState('Error')

            excp = err[1]
            message = str(excp.args[0]) if len(excp.args) == 1 else ''
            message = message.split("\n", 1)[0].strip()
            jrlEntry.setTestMessage(message)

            jrlFile.save()
        # end if
    # end def addError

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def addSuccess(self, test, unused = None):
        '''
        @copydoc pyharness.core.TestListener.addSuccess
        '''
        if (not isinstance(test, TestSuite)):

            testId = test.id()

            jrlFile = self._getJrlFile()
            jrlEntry = jrlFile.getLastEntry(testId)
            jrlEntry.setTestState('Ok')

            jrlFile.save()
        # end if
    # end def addSuccess
# end class JrlTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
