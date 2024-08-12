#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.xmlui

@brief  PyHarness XML output

This module contains the listeners that output the test progress to XML files.
The XML files format should be compatible with JUnit.

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.threadutils       import synchronized
from pyharness.arguments                 import KeywordArguments
from pyharness.core                      import TestListener
from pyharness.core                      import TestSuite
from pyharness.files.xmltestcase         import XmlTestResultFile
from pyharness.output.common             import FileTestListenerMixin
from os                                 import F_OK
from os                                 import access
from os                                 import listdir
from os                                 import makedirs
from os                                 import remove
from os.path                            import join
from threading                          import RLock
from time                               import localtime
from traceback                          import format_tb
import re

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class XmlTestListener(TestListener, FileTestListenerMixin):
    '''
    A TestListener class that can print xml test results to a stream.
    '''

    RELATIVE_PATH  = "xml"
    FILE_FORMAT    = "%sTestCase.xml"

    SYNCHRONIZATION_LOCK = RLock()

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        Constructor.

        @copydoc pyharness.core.TestListener.__init__
        '''
        super(XmlTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        self._xmlFiles = {}
    # end def __init__

    @staticmethod
    def _formatError(error):
        '''
        Formats an error to text

        @param error [in] (tuple) the error to format
        @return tuple(short message, traceback as string)
        '''
        return (error[1], '\n'.join(format_tb(error[2], None)))
    # end def _formatError


    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def _newEntry(self, testId,
                        startTime):
        '''
        Creates a new XmlTestCaseFile entry

        @param testId    [in] (str) The test id identifying the result
        @param startTime [in] (int)    The start time of the test
        @return The newly created, or cached, entry
        '''
        if (testId not in self._xmlFiles):
            outputFilePath = self._getOutputFilePath(testId)
            xmlFile = XmlTestResultFile(outputFilePath)
            xmlFile.setTestId(testId)
            xmlFile.setStartDate(startTime)
            self._xmlFiles[testId] = xmlFile
        # end if

        return self._xmlFiles[testId]
    # end def _newEntry

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def _getEntry(self, testId):
        '''
        Obtain an already-created XmlTestCaseFile entry

        @param testId [in] (str) The test id identifying the result
        @return The cached entry
        '''

        return self._xmlFiles[testId]
    # end def _getEntry

    @synchronized(SYNCHRONIZATION_LOCK)                                                                                 # pylint:disable=E0602
    def _delEntry(self, testId):
        '''
        Delete an already-created XmlTestCaseFile entry

        @param testId [in] (str) The test id identifying the result
        '''

        del self._xmlFiles[testId]
    # end def _delEntry

    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun

        Empties if needed all xml files
        '''
        if (not resumed):
            outputDir = join(self.outputdir, self.RELATIVE_PATH)

            if (self.args[KeywordArguments.KEY_ERASELOGS]):
                if (access(outputDir, F_OK)):

                    regex = re.compile(self.FILE_FORMAT % '.*')

                    # Erase _all_ tests in the directory.
                    for filename in listdir(outputDir):
                        if regex.match(filename.lower()):
                            remove(join(outputDir, filename))
                        # end if
                    # end for
                # end if
            # end if

            if (not resumed):
                if (not access(outputDir, F_OK)):
                    makedirs(outputDir)
                # end if
            # end if
        # end if
    # end def startRun

    def resetTest(self, test, context):                                                                                 # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.resetTest
        '''
        testId = test.id()
        outputFilePath = self._getOutputFilePath(testId)
        if (access(outputFilePath, F_OK)):
            remove(outputFilePath)
        # end if
    # end def resetTest

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        if (not isinstance(test, TestSuite)):
            # Create a new entry for this test
            testId = test.id()
            self._newEntry(testId, localtime())
        # end if
    # end def startTest

    def stopTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.stopTest
        '''
        if (not isinstance(test, TestSuite)):

            testId = test.id()

            entry = self._getEntry(testId)

            # An uninitialized state is theoretically not possible.
            # It only occurs in ONE unit test for the framework.
            if (entry.getState() is not None):
                entry.setStopDate(localtime())
                description = ""
                if (hasattr(test, 'fullDescription')):
                    description = test.fullDescription()
                elif (hasattr(test, '_testMethodDoc')):
                    description = getattr(test, '_testMethodDoc')
                # end if

                if description is None:
                    description = ""
                # end if

                entry.setDescription(description)
                entry.save()
            # end if

            self._delEntry(testId)
        # end if
    # end def stopTest

    def addPerformanceData(self, test, key, value, unit=None):
        '''
        @copydoc pyharness.core.TestListener.addPerformanceData
        '''
        testId = test.id()
        entry = self._getEntry(testId)

        perfData = entry.getPerfData()
        elements = perfData.setdefault(key, [])
        elements.append((value, unit,))
    # end def addPerformanceData

    def addSuccess(self, test, unused = None):
        '''
        @copydoc pyharness.core.TestListener.addSuccess
        '''

        testId = test.id()
        entry = self._getEntry(testId)
        entry.setState('success')
    # end def addSuccess

    def addTestCase(self, test, testCase, author=None, comment=None):
        '''
        @copydoc pyharness.core.TestListener.addTestCase
        '''
        testId = test.id()
        entry = self._getEntry(testId)

        entry.getTestCases()[testCase] = (author, comment)
    # end def addTestCase

    def addError(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addError
        '''
        testId = test.id()
        entry = self._getEntry(testId)

        # The TestListener MUST NOT keep a reference to the traceback
        # Doing so would prevent the garbage collection from occurring, and would result:
        # - In increased memory consumption.
        # - In non-released locks, leading to deadlocks.}
        message, error = self._formatError(err)
        entry.setState('error')
        try:
            text = str(message[-1])
        except Exception:                                                                                               # pylint:disable=W0703
            text = str(message)
        # end try
        entry.setMessage(text)
        entry.setTraceback(error)
    # end def addError

    def addFailure(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addFailure
        '''
        testId = test.id()
        entry = self._getEntry(testId)

        # The TestListener MUST NOT keep a reference to the traceback
        # Doing so would prevent the garbage collection from occurring, and would result:
        # - In increased memory consumption.
        # - In non-released locks, leading to deadlocks.}
        message, error = self._formatError(err)
        entry.setState('failure')

        try:
            text = str(message[-1])
        except Exception:                                                                                               # pylint:disable=W0703
            text = str(message)
        # end try
        entry.setMessage(text)
        entry.setTraceback(error)
    # end def addFailure

    def getResultDirPath(self):
        '''
        @copydoc pyharness.output.common.FileTestListenerMixin._resultDirPath
        '''
        return self._resultDirPath()
    # end def getResultDirPath
# end class XmlTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
