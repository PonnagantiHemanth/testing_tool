#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.pyunitui

@brief PyUnit-compatible xml output

@author christophe.roquebert

@date   2018/06/10
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                            import abspath
from pyharness.arguments                import KeywordArguments
from pyharness.core                     import TestListener
from os                                 import F_OK
from os                                 import access
from os                                 import listdir
from os                                 import makedirs
from os                                 import remove
from os.path                            import join
from time                               import time
from traceback                          import format_tb
from xml.dom.minidom                    import getDOMImplementation

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class PyUnitTestListener(TestListener):
    '''
    A TestListener that outputs test results to a pyunit-compatible xml output
    '''

    RELATIVE_PATH = 'pyunit'
    FILE_EXTENSION = 'xml'

    def __init__(self, descriptions, verbosity, outputdir, args):
        '''
        Constructor

        @copydoc pyharness.core.TestListener.__init__
        '''
        super(PyUnitTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        # A map testId -> (state, traceback or None, type or None, time)
        self._results = {}
        self._time    = None
    # end def __init__

    def __resultDirPath(self):
        '''
        Builds the path to the directory containing the log files

        @return The file path to the test log.
        '''
        result = abspath(join(self.outputdir, self.RELATIVE_PATH))

        return result
    # end def __resultDirPath

    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun

        Empties if needed all xml files
        '''
        if (not resumed):
            outputDir = self.__resultDirPath()

            if (self.args[KeywordArguments.KEY_ERASELOGS]):
                if (access(outputDir, F_OK)):
                    # Erase _all_ tests in the directory.
                    for filename in listdir(outputDir):
                        if (filename.lower().endswith('.%s' % self.FILE_EXTENSION)):
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

            if (not resumed):
                self._results.clear()
                self._time = time()
            # end if
        # end if
    # end def startRun

    @staticmethod
    def _formatError(error):
        '''
        Formats an error to text

        @param error [in] (tuple) the error to format
        @return tuple(short message, traceback as string)
        '''
        return (error[1], '\n'.join(format_tb(error[2], None)))
    # end def _formatError

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        self._results[test.id()] = ['unknown', None, None, time()]
    # end def startTest

    def addSuccess(self, test, unused=None):
        '''
        @copydoc pyharness.core.TestListener.addSuccess
        '''
        self._results.setdefault(test.id(), ['unknown', None, None, 0])[0] = 'success'
    # end def addSuccess

    def addFailure(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addFailure
        '''
        _, error = self._formatError(err)
        entry = self._results.setdefault(test.id(), ['unknown', None, None, 0])
        entry[0] = 'failure'
        entry[1] = error
        entry[2] = '.'.join((err[0].__class__.__module__, err[0].__class__.__name__))
    # end def addFailure

    def addError(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addError
        '''
        _, error = self._formatError(err)
        entry = self._results.setdefault(test.id(), ['unknown', None, None, 0])
        entry[0] = 'error'
        entry[1] = error
        entry[2] = '.'.join((err[0].__class__.__module__, err[0].__class__.__name__))
    # end def addError

    def stopTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.stopTest
        '''
        entry = self._results.setdefault(test.id(), ['unknown', None, None, 0])
        entry[3] = time() - entry[3]
    # end def stopTest

    def stopRun(self, result, suspended):                                                                               # pylint:disable=W0613,R0914
        '''
        @copydoc pyharness.core.TestListener.stopRun
        '''
        if (not suspended):
            totalTime = time() - self._time
            dom = getDOMImplementation()
            doc = dom.createDocument(None, "testsuite", None)

            values = list(self._results.values())
            allCount   = len(values)
            errorCount = len([t for t in values if t[0] == 'error'])
            failureCount = len([t for t in values if t[0] == 'failure'])
            testSuiteElement =  doc.getElementsByTagName('testsuite')[0]
            testSuiteElement.setAttribute('errors', str(errorCount))
            testSuiteElement.setAttribute('failures', str(failureCount))
            testSuiteElement.setAttribute('tests', str(allCount))
            testSuiteElement.setAttribute('time', "%.3f" % totalTime)


            for testId, (state, traceback, classType, testTime) in self._results.items():
                className, name = testId.rsplit('.', 1)

                testCaseElement = doc.createElement('testcase')
                testCaseElement.setAttribute('classname', className)
                testCaseElement.setAttribute('name', name)
                testCaseElement.setAttribute('time', '%.3f' % testTime)

                stateElement = None
                if (state == 'failure'):
                    stateElement = doc.createElement('failure')
                elif (state == 'error'):
                    stateElement = doc.createElement('error')
                # end if

                if (stateElement is not None):
                    stateElement.setAttribute('type', classType)
                    textNode = doc.createTextNode(traceback)
                    stateElement.appendChild(textNode)

                    testCaseElement.appendChild(stateElement)
                # end if

                testSuiteElement.appendChild(testCaseElement)
            # end for

            stdoutElement = doc.createElement('system-out')
            testSuiteElement.appendChild(stdoutElement)

            stderrElement = doc.createElement('system-err')
            testSuiteElement.appendChild(stderrElement)

            # Create the output file
            outputFilePath = join(self.__resultDirPath(), 'results.xml')
            with open(outputFilePath, "w+") as outputFile:
                doc.writexml(outputFile, '', '  ', '\n')
            # end with
        # end if
    # end def stopRun
# end class PyUnitTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
