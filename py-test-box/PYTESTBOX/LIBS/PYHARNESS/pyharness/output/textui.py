#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.textui

@brief PyHarness console output

This module contains the listeners that output the test progress to the console.

@author christophe.roquebert

@date   2018/09/11
'''

#Parts of the code come from Steve Purcell's pyunit framework.
#
#Copyright (c) 1999, 2000, 2001 Steve Purcell
#This module is free software, and you may redistribute it and/or modify
#it under the same terms as Python itself, so long as this copyright message
#and disclaimer are retained in their original form.
#
#IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
#SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
#THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
#DAMAGE.
#
#THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
#LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
#PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
#AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
#SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core                      import TYPE_ERROR
from pyharness.core                      import TYPE_FAILURE
from pyharness.core                      import TYPE_START
from pyharness.core                      import TYPE_STARTRUN
from pyharness.core                      import TYPE_STOPRUN
from pyharness.core                      import TYPE_SUCCESS
from pyharness.core                      import TYPE_SKIPPED
from pyharness.core                      import TYPE_EXP_FAIL
from pyharness.core                      import TestCase
from pyharness.core                      import TestListener
from pyharness.core                      import TestSuite
from pyharness.core import _LEVEL_ERROR
from pyharness.core import _LEVEL_TRACE
from pyharness.selector import services
from threading                          import RLock
from threading                          import currentThread
from time                               import time
import re
import sys
import traceback

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class _WritelnDecorator(object):
    '''
    Used to decorate file-like objects with a handy 'writeln' method
    '''

    def __init__(self, stream):
        '''
        Constructor

        @param  stream [in] (stream) The stream to decorate
        '''
        self.stream = stream
    # end def __init__

    def __getattr__(self, attr):
        '''
        Redirect decorated attributes to the source stream.

        @param  attr [in] (str) The attribute to obtain

        @return The attribute extracted drom the source stream.
        '''
        return getattr(self.stream, attr)
    # end def __getattr__

    def writeln(self, *args):
        '''
        Additional method for writing an EOL

        @option args [in] (tuple) The arguments of the write method.
        '''
        if (args):
            self.stream.write(*args)
        # end if
        self.stream.write('\n') # text-mode streams translate to \r\n if needed
    # end def writeln
# end class _WritelnDecorator

class TextTestListener(TestListener):
    '''
    A test result class that can print formatted text results to a stream.

    Used by TextTestRunner.
    '''

    separator0 = '#' * 70
    separator1 = '=' * 70
    separator2 = '-' * 70

    THREAD_SLOTS = []
    SYNCHRONIZATION_LOCK = RLock()

    def __init__(self, descriptions, verbosity, outputdir, args = False):
        '''
        Constructor.

        @copydoc pyharness.core.TestListener.__init__
        '''

        super(TextTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        self.stream             = _WritelnDecorator(sys.stdout)
        self.loghandlers        = {}

        self.testsRun           = 0
        self.testsFailed        = 0
        self.testsErrored       = 0
        self.testsSkipped       = 0
        self.startTime          = None

        self._threads = args.get('threads', None)
        
        self.max_lines_in_console = 4 if verbosity == _LEVEL_TRACE else 1 if verbosity == _LEVEL_ERROR else None
    # end def __init__

    def attach(self, testResult):
        '''
        @copydoc pyharness.core.TestListener.attach
        '''
        with self.SYNCHRONIZATION_LOCK:
            testResult.addListener(TYPE_STARTRUN, self.startRun)
            testResult.addListener(TYPE_START,    self.startTest)
            testResult.addListener(TYPE_ERROR,    self.addError)
            testResult.addListener(TYPE_FAILURE,  self.addFailure)
            testResult.addListener(TYPE_SUCCESS,  self.addSuccess)
            testResult.addListener(TYPE_STOPRUN,  self.stopRun)
            testResult.addListener(TYPE_SKIPPED,  self.addSkip)
            testResult.addListener(TYPE_EXP_FAIL, self.addExpectedFailure)
        # end with
    # end def attach

        # Ignore other listeners: bugs and TestCases, as they are not needed for
        # progress information

    def detach(self, testResult):
        '''
        @copydoc pyharness.core.TestListener.detach
        '''
        with self.SYNCHRONIZATION_LOCK:
            testResult.removeListener(TYPE_STARTRUN, self.startRun)
            testResult.removeListener(TYPE_START,    self.startTest)
            testResult.removeListener(TYPE_ERROR,    self.addError)
            testResult.removeListener(TYPE_FAILURE,  self.addFailure)
            testResult.removeListener(TYPE_SUCCESS,  self.addSuccess)
            testResult.removeListener(TYPE_STOPRUN,  self.stopRun)
            testResult.removeListener(TYPE_SKIPPED,  self.addSkip)
            testResult.removeListener(TYPE_EXP_FAIL, self.addExpectedFailure)
        # end with
    # end def detach

    def _addThreadToSlots(self):
        '''
        Add the current thread to the list of traced threads
        '''

        with self.SYNCHRONIZATION_LOCK:
            index = 0
            innerThread = currentThread()
            for thread in self.THREAD_SLOTS:
                if thread is innerThread:
                    break
                # end if
                index += 1
            else:
                for index in range(len(self.THREAD_SLOTS)):
                    if self.THREAD_SLOTS[index] is  None:
                        self.THREAD_SLOTS[index] = innerThread
                        break
                    # end if
                else:
                    self.THREAD_SLOTS.append(innerThread)
                # end for
            # end for
        # end with
    # end def _addThreadToSlots

    def _removeThreadFromSlots(self):
        '''
        Remove the thread from the slots.
        '''
        with self.SYNCHRONIZATION_LOCK:
            index = 0
            innerThread = currentThread()
            for index in range(len(self.THREAD_SLOTS)):
                thread = self.THREAD_SLOTS[index]
                if thread is innerThread:
                    self.THREAD_SLOTS[index] = None
                    break
                # end if
            # end for
        # end with
    # end def _removeThreadFromSlots

    def _printMessage(self, messageType, test, err=None):
        '''
        Write a summary of the running threads
        - A starting test is written with:      '+'
        - A running thread is written with:     '|'
        - A non-running thread is written with: ' '
        - A Success is written:                 'ok'
        - A Failure or error is completely traced

        @param  messageType [in] (str) The message type (ok, *, +)
        @param  test        [in] (TestCase) The test being traced
        @option err         [in] (excp) The error
        '''
        # This is a standard message
        with self.SYNCHRONIZATION_LOCK:
            if (self._threads == '1'):

                if (messageType == ' + '):
                    message = '\n%s ... ' % (test.id())
                elif (messageType == 'ok'):
                    message = 'ok'
                    if test.warning_occurred:
                        message += ' (warning)'
                    # end if
                elif (messageType == 'skipped'):
                    message = 'skipped \'%s\'' % (err)
                elif (err is not None):
                    message = self._printError(messageType, test, err)
                else:
                    raise ValueError('Unexpected TestListener state')
                # end if

                self.stream.write(message)
                self.stream.flush()
            else:
                if (err is None or messageType == 'skipped'):
                    message = ""
                    if messageType == 'skipped':
                        messageType = 'skp'
                    innerThread = currentThread()
                    for thread in self.THREAD_SLOTS:
                        if thread is innerThread:
                            message += messageType
                            message += " " * (3 - len(messageType))
                        elif (thread is None):
                            message += "   "
                        else:
                            message += " | "
                        # end if
                    # end for
                    message += test.id()
                else:
                    message = self._printError(messageType, test, err)
                # end if

                self.stream.writeln(message)
                self.stream.flush()
            # end if
        # end with
    # end def _printMessage

    def getDescription(self, test):
        '''
        Obtains a short description from the test.

        @param  test [in] (TestCase) The test to decribe.

        @note   This description extracts uses the test.shortDescription to
                extract the test method docstring, if available.

        @return Description of the test
        '''
        if self.descriptions:
            return test.shortDescription() or str(test)
        else:
            return str(test)
        # end if
    # end def getDescription

    def startRun(self, context, resumed):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.startRun
        '''
        if not resumed:
            self.startTime = time()
        # end if
    # end def startRun

    def stopRun(self, result, suspended):                                                                               # pylint:disable=W0613
        '''
        @copydoc pyharness.core.TestListener.stopRun
        '''
        if not (suspended):
            timeTaken = time() - self.startTime

            self.stream.write("\n")
            self.stream.write("Ran %d test%s in %.3fs\n"
                            % (self.testsRun,
                               (self.testsRun == 1) and "" or "s",
                               timeTaken))

            if ((self.testsErrored + self.testsFailed) > 0):
                self.stream.write("FAILED (")

                if self.testsFailed:
                    self.stream.write("failures=%d" % (self.testsFailed,))
                # end if

                if self.testsErrored:
                    if self.testsFailed:
                        self.stream.write(", ")
                    # end if
                    self.stream.write("errors=%d" % (self.testsErrored,))
                # end if
                
                self.stream.write(")")
            else:
                self.stream.write("OK")
            # end if
            
            if self.testsSkipped:
                self.stream.write(" (skipped=%d)" % (self.testsSkipped,))
            # end if
            
            self.stream.write("\n")

            self.stream.write(services.get_filtering_summary())

        # end if
    # end def stopRun

    def startSuite(self, test):
        '''
        Test suite start notification.

        @param  test [in] (TestSuite) The test suite that starts.
        '''
        self.stream.writeln(self.separator0)
        self.stream.writeln("# Test suite: %s" % (test.id(),))
    # end def startSuite

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        if (isinstance(test, TestSuite)):
            self.startSuite(test)
        else:
            with self.SYNCHRONIZATION_LOCK:
                self._addThreadToSlots()
                self._printMessage(' + ', test)
            # end with

            self.testsRun += 1
        # end if
    # end def startTest

    def addSuccess(self, test, unused=None):
        '''
        @copydoc pyharness.core.TestListener.addSuccess
        '''
        with self.SYNCHRONIZATION_LOCK:
            self._printMessage("ok", test)
            self._removeThreadFromSlots()
        # end with
    # end def addSuccess

    def addError(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addError
        '''

        with self.SYNCHRONIZATION_LOCK:
            self._printMessage("ERROR", test, err)
            self._removeThreadFromSlots()
        # end with

        self.testsErrored += 1
    # end def addError

    def addFailure(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addFailure
        '''
        with self.SYNCHRONIZATION_LOCK:
            self._printMessage("FAIL", test, err)
            self._removeThreadFromSlots()
        # end with

        self.testsFailed += 1
    # end def addFailure
    
    def addExpectedFailure(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addFailure
        '''
        with self.SYNCHRONIZATION_LOCK:
            self._printMessage("expected failure", test, err)
            self._removeThreadFromSlots()
        # end with
    # end def addExpectedFailure

    def addSkip(self, test, err):
        '''
        @copydoc pyharness.core.TestListener.addSkip
        '''
        with self.SYNCHRONIZATION_LOCK:
            self._printMessage("skipped", test, err)
            self._removeThreadFromSlots()
        # end with

        self.testsSkipped += 1
        self.testsRun -= 1
    # end def addSkip

    REGEX = re.compile(r".*\.py.?\", line [0123456789]+, in (\w+).*")

    def _printError(self, flavour, test, err):
        '''
        Prints a detailed error message.

        @param  flavour [in] (str) The type of error message.
        @param  test    [in] (TestCase) The test that caused the error.
        @param  err     [in] (excp) The error cause.

        @return The formatted message string.
        '''

        # Print the first line, that contains the text explanation extracted
        # from the docstring
        lines = []
        lines.append(self.separator1)
        lines.append("%s: %s" % (flavour, self.getDescription(test)))
        lines.append(self.separator2)

        tracelist = traceback.format_exception(*err)[-self.max_lines_in_console:] \
            if self.max_lines_in_console is not None else traceback.format_exception(*err)
        newtrace = []

        # Print elements from the stack trace, excluding parts of the stack
        # that are not relevant to the test.
        dropped = False
        for element in reversed(tracelist):
            newtrace.insert(0, element)

            if (not dropped):
                found = self.REGEX.search(element)
                if (not found is None):
                    value = found.group(1)
                    if (value in TestCase.TRACEBACK_CODENAMES):
                        newtrace = tracelist[-1:]
                        dropped = True
                    # end if
                # end if
            # end if
        # end for

        for line in newtrace:
            for innerLine in line.rsplit("\n", 1)[:-1]:
                lines.append("%s" % (innerLine,))
            # end for
        # end for

        lines.append(self.separator2)

        return "\n".join(lines)
    # end def _printError
# end class TextTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
