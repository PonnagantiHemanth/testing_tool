#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.core
:brief: Core PyHarness implementation
        This module is the core of the PyHarness framework.
        It contains base classes for TestCases, TestSuites, loading and running tests, as well listeners notification.
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/09/11
"""

# Parts of the code come from Steve Purcell's pyunit framework.
# The following copyright only applies to the original pyunit code.
#
# Python Test Harness
# This module is free software, and you may redistribute it and/or modify
# it under the same terms as Python itself, so long as this copyright message
# and disclaimer are retained in their original form.
#
# IN NO EVENT SHALL THE AUTHOR BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT,
# SPECIAL, INCIDENTAL, OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE USE OF
# THIS CODE, EVEN IF THE AUTHOR HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH
# DAMAGE.
#
# THE AUTHOR SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE.  THE CODE PROVIDED HEREUNDER IS ON AN "AS IS" BASIS,
# AND THERE IS NO OBLIGATION WHATSOEVER TO PROVIDE MAINTENANCE,
# SUPPORT, UPDATES, ENHANCEMENTS, OR MODIFICATIONS.

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
import unittest
from functools import reduce
from functools import wraps
from imp import get_suffixes
from os import listdir
from os.path import exists
from os.path import isdir
from os.path import join
from os.path import normpath
from os.path import sep
from os.path import splitext
from threading import Lock
from threading import RLock
from threading import Semaphore
from threading import local
from traceback import format_exception
from types import FunctionType
from types import MethodType
from types import ModuleType
from unittest import TestCase as UnitTestCase
from unittest import TestSuite as UnitTestSuite
# noinspection PyUnresolvedReferences
# noinspection PyProtectedMember
from unittest.case import _Outcome
from warnings import warn
from warnings import warn_explicit

from pyharness.fixtures import fixtures
from pyharness.selector import REVERSED_MARK
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import isFeatureReversed
from pyharness.selector import services
from pylibrary.tools.importutils import importFqn
from pylibrary.tools.threadutils import Task
from pylibrary.tools.threadutils import ThreadedExecutor
from pylibrary.tools.threadutils import synchronized

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
# Message level
_LEVEL_BASE = 1  # Base level, must not be 0

_LEVEL_DEBUG = _LEVEL_BASE + 1

_LEVEL_RAW = _LEVEL_DEBUG + 1
_LEVEL_COMMAND = _LEVEL_RAW + 1

_LEVEL_TRACE = _LEVEL_COMMAND + 1
_LEVEL_INFO = _LEVEL_TRACE + 1
_LEVEL_TITLE3 = _LEVEL_INFO + 1
_LEVEL_TITLE2 = _LEVEL_TITLE3 + 1
_LEVEL_TITLE1 = _LEVEL_TITLE2 + 1
_LEVEL_SEPARATOR = _LEVEL_TITLE1 + 1

_LEVEL_ERROR = _LEVEL_SEPARATOR + 1
_LEVEL_MAX = _LEVEL_ERROR

_ALL_LEVELS = list(range(_LEVEL_BASE, _LEVEL_MAX+1))

# Message mask
_MASK_LEVEL = 0x0F
_MASK_ALWAYS = 0x10

# Message type
TYPE_STOPRUN = -7  # End run event
TYPE_STARTRUN = -6  # Start run event
TYPE_LOG = -5  # Logging event
TYPE_TEST_DATA = -4  # Test data logging event
TYPE_PERFORMANCE = -3  # Performance logging event
TYPE_STOP = -2  # End test event
TYPE_START = -1  # Start test event
TYPE_SUCCESS = 0  # Success
TYPE_FAILURE = 1  # Failure, checked result
TYPE_ERROR = 2  # Error, never used in an exception.
TYPE_BUG = 3  # Bug, checked result.
TYPE_TESTCASES = 4  # TestCases, traced result.
TYPE_SKIPPED = 5  # Test skipped
TYPE_EXP_FAIL = 6  # Expected failure

NOTIFICATION_TYPES = (TYPE_PERFORMANCE,
                      TYPE_STOP,
                      TYPE_START,
                      TYPE_SUCCESS,
                      TYPE_FAILURE,
                      TYPE_ERROR,
                      TYPE_BUG,
                      TYPE_TESTCASES,
                      TYPE_SKIPPED,
                      TYPE_EXP_FAIL,
                      )

# Python suffixes
_SUFFIXES = [s[0] for s in get_suffixes()]


def failfast(method):
    @wraps(method)
    def inner(self, *args, **kw):
        if getattr(self, 'failfast', False):
            self.stop()
        # end if
        return method(self, *args, **kw)
    # end def inner
    return inner
# end def failfast


class TestException(AssertionError):
    """
    Common wrapper for errors, failures, bugs...
    """
    def __init__(self, message_type, message_text):
        """
        :param message_type: The message type
        :type message_type: ``int``
        :param message_text: The exception message
        :type message_text: ``str``
        """
        AssertionError.__init__(self, message_text)

        self.type = message_type
    # end def __init__
# end class TestException


class TestAccess(object):
    """
    A simplified description of a test.

    This provides simplified access to the core items, to be used in the Sorters and Filter.

    This way, Sorters and Filter can access properties of the test, without risk of corrupting the inner state.
    """

    # noinspection PyPep8Naming
    def __init__(self, testId, testLevels, testRunHistory, staticTestCases):
        """
        :param testId: The test id
        :type testId: ``str``
        :param testLevels: The list of levels associated with the test.
        :type testLevels: ``list[str]``
        :param testRunHistory: The run history.
        :type testRunHistory: ``list[tuple[str,long,long,str]]``
        :param staticTestCases: [in] (list<string>) The list of TestCases implemented by the test.
        :type staticTestCases: ``str``
        """
        self._testId = testId
        self._testLevels = testLevels
        self._runHistory = testRunHistory
        self._staticTestCases = staticTestCases
    # end def __init__

    # noinspection PyPep8Naming
    def getTestId(self):
        """
        Obtain the test id

        :return: The test id
        :rtype: ``str``
        """
        return self._testId
    # end def getTestId

    # noinspection PyPep8Naming
    def getTestLevels(self):
        """
        Obtain the test levels.

        :return: The list of levels associated with the test.
        :rtype: ``list[str]``
        """
        return self._testLevels
    # end def getTestLevels

    # noinspection PyPep8Naming
    def getRunHistory(self):
        """
        Obtain  the available run history for the test.

        The run history is a sequence of tuples, where each tuple contains:
        - The test state (as a string)
        - The test start date (as a long), or None if unavailable
        - The test end date (as a long), or None if unavailable
        - The test comment (as a string), or None if unavailable

        The run history is sorted by start date, then by end date

        :return: A tuple(state, startDate, endDate, comment)
        :rtype: ``tuple[str, int, int, str]``
        """
        return self._runHistory
    # end def getRunHistory

    # noinspection PyPep8Naming
    def getStaticTestCases(self):
        """
        Obtain  the list of static TestCases implemented by the test.

        :return: A list of string
        :rtype: ``list[str]``
        """
        return self._staticTestCases
    # end def getStaticTestCases

    def __str__(self):
        """
        Convert the current object to a readable string.

        :return: The current object, as a string.
        :rtype: ``str``
        """
        return "%s, %s" % (self._testId, self._testLevels,)
    # end def __str__

    __repr__ = __str__
# end class TestAccess


class TestListener(object):
    """
    Base implementation of a TestListener

    Test listeners are used by the validation framework to notify external
    observers of events that occur in the validation.
    """

    TYPE_TO_METHOD_MAPPING = {
                                TYPE_STOPRUN:     "stopRun",
                                TYPE_STARTRUN:    "startRun",
                                TYPE_START:       "startTest",
                                TYPE_ERROR:       "addError",
                                TYPE_FAILURE:     "addFailure",
                                TYPE_SUCCESS:     "addSuccess",
                                TYPE_STOP:        "stopTest",
                                TYPE_LOG:         "log",
                                TYPE_PERFORMANCE: "addPerformanceData",
                                TYPE_TEST_DATA:   "add_test_data",
                                TYPE_TESTCASES:   "addTestCase",
                                }

    # Whether this TestListener is mandatory (i.e. is always present,
    # cannot be disabled by the user
    MANDATORY = False

    # Whether this TestListener is visible in the UI
    VISIBLE = True

    # Whether this TestListener's error block the run.
    ERRORS_SHOULD_BLOCK = False

    def __init__(self, descriptions, verbosity, outputdir, args):
        """
        :param descriptions: Flag indicating whether the test descriptions are output.
                             At the lowest setting, only the test id is printed.
                             At higher settings, a complete test description is printed.
        :type descriptions: ``int|None``
        :param verbosity: The verbose level of the output
        :type verbosity: ``int|None``
        :param outputdir: The output directory
        :type outputdir: ``str|None``
        :param args: Positional arguments.
        :type args: ``tuple|None``
        """
        self.descriptions = descriptions
        self.verbosity = verbosity
        self.outputdir = outputdir if outputdir is None else normpath(outputdir)
        self.args = args
        self.ignoreCollection = True
    # end def __init__

    # noinspection PyPep8Naming
    def attach(self, testResult):
        """
        Attach the test listener to the test result

        Note that the default implementation uses introspection to automatically
        add the listeners. If you follow the naming conventions, it is not
        necessary to re-implement this method.

        :param testResult: The TestResult to attach to.
        :type testResult: ``TestResult``

        Example:
        @code
        def attach(self, testResult):
            testResult.addListener(TYPE_START, self.startTest)
            testResult.addListener(TYPE_ERROR, self.addError)
            testResult.addListener(TYPE_FAILURE, self.addFailure)
            testResult.addListener(TYPE_SUCCESS, self.addSuccess)
            testResult.addListener(TYPE_STOP, self.stopTest)
        # end def attach
        @endcode
        """
        for key, value in self.TYPE_TO_METHOD_MAPPING.items():
            if getattr(self.__class__, value) != getattr(TestListener, value):
                testResult.addListener(key, getattr(self, value), propagateException=self.ERRORS_SHOULD_BLOCK)
            # end if
        # end for
    # end def attach

    # noinspection PyPep8Naming
    def detach(self, testResult):
        """
        Detache the test listener from the test result

        :param testResult: The TestResult to detach from.
        :type testResult: ``TestResult``

        Example:
        @code
        def detach(self, testResult):
            testResult.removeListener(TYPE_START, self.startTest)
            testResult.removeListener(TYPE_ERROR, self.addError)
            testResult.removeListener(TYPE_FAILURE, self.addFailure)
            testResult.removeListener(TYPE_SUCCESS, self.addSuccess)
            testResult.removeListener(TYPE_STOP, self.stopTest)
        # end def detach
        @endcode
        """
        for key, value in self.TYPE_TO_METHOD_MAPPING.items():
            if getattr(self.__class__, value) != getattr(TestListener, value):
                testResult.removeListener(key, getattr(self, value))
            # end if
        # end for
    # end def detach

    # noinspection PyPep8Naming
    def startRun(self, context, resumed):
        """
        Handle the startRun notification.

        :param context: The context in which the tests will run
        :type context: ``TestResult``
        :param resumed: Flag indicating whether the run was started from scratch, or resumed
        :type resumed: ``bool``
        """
        pass
    # end def startRun

    # noinspection PyPep8Naming
    def resetTest(self, test, context):
        """
        Reset the test state

        :param test: The test to reset
        :type test: ``Test``
        :param context: The context in which the tests will run
        :type context: ``Context``
        """
        pass
    # end def resetTest

    # noinspection PyPep8Naming
    def startTest(self, test):
        """
        Handle the startTest notification, and prints the progress if necessary.

        :param test: The starting test
        :type test: ``Test``
        """
        pass
    # end def startTest

    # noinspection PyPep8Naming
    def stopTest(self, test):
        """
        Called when the given test has been run

        :param test: The test that terminated.
        :type test: ``Test``
        """
        pass
    # end def stopTest

    # noinspection PyPep8Naming
    def stopRun(self, result, suspended):
        """
        Test run stop notification.

        :param result: The test results.
        :type result: ``TestResult``
        :param suspended: Flag indicating whether the run was suspended or terminated.
        :type suspended: ``bool``
        """
        pass
    # end def stopRun

    # noinspection PyPep8Naming
    def addSuccess(self, test, unused=None):
        """
        Handle the addSuccess notification.

        :param test: The test that succeeded
        :type test: ``Test``
        :param unused: Ignored parameter - OPTIONAL
        :type unused: ``str|None``
        """
        pass
    # end def addSuccess

    # noinspection PyPep8Naming
    def addError(self, test, err):
        """
        Handle the addError notification.

        :param test: The test that cause the error
        :type test: ``Test``
        :param err: The error to add
        :type err: ``tuple``
        """
        pass
    # end def addError

    # noinspection PyPep8Naming
    def addFailure(self, test, err):
        """
        Handle the addFailure notification.

        :param test: The test that failed
        :type test: ``Test``
        :param err: The failure to add
        :type err: ``tuple``
        """
        pass
    # end def addFailure

    # noinspection PyPep8Naming
    def acceptLog(self, level):
        """
        Test message level vs. verbosity

        :param level: The level at which to log.
        :type level: ``int``

        :return: Flag indicating whether the testlistener accepts the current log level
        :rtype: ``bool``
        """
        return level >= self.verbosity
    # end def acceptLog

    def log(self, test, level, msg, *args, **kwargs):
        """
        Handle the log notification.

        This logs a given message to the various log files for the specified test.
        Note that the preferred use of the log API is to post-format the message.

        For instance, do not do:
        @code
        self.log(testId, logLevel, "Error at %s: %s, %s, %s" % (index, s1, s2, s3))
        @endcode
        because this evaluates the string even if no log is written.
        Instead, do
        @code
        self.log(testId, logLevel, "Error at %s: %s, %s, %s", index, s1, s2, s3)
        @endcode
        This way, the string will only be formatted if necessary.

        :param test: The test for which to log the information.
        :type test: ``Test``
        :param level: The level at which to log.
        :type level: ``int``
        :param msg: The message to log.
        :type msg: ``str``
        :param args: Positional arguments.
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        pass
    # end def log

    # noinspection PyPep8Naming
    def addPerformanceData(self, test, key, value, unit=None):
        """
        Called when the given test wants to add a performance data to the pool.

        :param test: The test for which to log the information.
        :type test: ``Test``
        :param key: Key to add
        :type key: ``str``
        :param value: Value to add
        :type value: ``int,float``
        :param unit: The unit of the traced value - OPTIONAL
        :type unit: ``str``
        """
        pass
    # end def addPerformanceData

    def add_test_data(self, test, data):
        """
        Called when the given test wants to add a test data to the pool.

        :param test: The test for which to log
        :type test: ``PyHarnessCase``
        :param data: Test data string to add to the log
        :type data: ``str``
        """
        pass
    # end def add_test_data

    # noinspection PyPep8Naming
    def addTestCase(self, test, testCase, author=None, comment=None):
        """
        Called when a test has verified a TestCase

        :param test: The test that verified the ``TestCase``
        :type test: ``Test``
        :param testCase: The testcase that was verified
        :type testCase: ``str``
        :param author: The author of the validation (None if automatic) - OPTIONAL
        :type author: ``str``
        :param comment: A comment on the validation - OPTIONAL
        :type comment: ``str``
        """
        pass
    # end def addTestCase

    def synchronize(self, listeners):
        """
        Synchronize self with other listeners if needed

        :param listeners: List of listeners
        :type listeners: ``list[Listener]``
        """
        pass
    # end def synchronize
# end class TestListener


class TestResult(object):
    """
    Holder for test result information.

    Test results are automatically managed by the TestCase and TestSuite
    classes, and do not need to be explicitly manipulated by writers of tests.

    Each instance holds the total number of tests run, and collections of
    failures and errors that occurred among those test runs. The collections
    contain tuples of (testCase, exceptioninfo), where exceptioninfo is a
    tuple of values as returned by sys.exc_info().
    """
    def __init__(self):
        # contains a dict: key: resulttype -> (test, err)
        self.results = {}
        self.listeners = {}

        self.failfast = False
        self.failures = []
        self.errors = []
        self.testsRun = 0
        self.skipped = []
        self.expectedFailures = []
        self.unexpectedSuccesses = []
        self.shouldStop = 0
    # end def __init__

    # noinspection PyPep8Naming
    def addListener(self, listenerType, listenerFunction, propagateException=False):
        """
        Add a listener to this test result, thus removing the need to derive
        a new TestResult instance for each output.

        It also simplifies the implementation of multiple outputters on
        a single run.

        :param listenerType: The type of listener to add
        :type listenerType: ``int|str``
        :param listenerFunction: The callback function to call (depends on the type listened to)
        :type listenerFunction: ``function``
        :param propagateException: Flag indicating whether the exception should be propagated or not - OPTIONAL
        :type propagateException: ``bool``
        """
        listeners_for_type = self._getListeners(listenerType)

        # Wrap the listener function in an exception absorber
        class Absorber(object):
            """
            Absorb exception instead of propagating them.
            """

            def __init__(self, listener_function):
                """
                :param listener_function: The callback to wrap.
                :type listener_function: ``callable``
                """
                self.listenerFunction = listener_function
            # end def __init__

            def __hash__(self):
                """
                Obtain  a hash for the current object

                :return: (int) A hash of the current object.
                """
                return hash(self.listenerFunction)
            # end def __hash__

            def __call__(self, *args, **kwargs):
                """
                If an exception occurs, use the warning system to display them, then proceed

                :param args: Positional arguments
                :type args: ``tuple``
                :param kwargs: Keyword arguments
                :type kwargs: ``dict``

                :return: Function result
                :rtype: ``int|None``
                """
                try:
                    return self.listenerFunction(*args, **kwargs)

                except Exception as exception:
                    # Obtain the 'best' exception location
                    try:
                        _, _, exc_traceback = sys.exc_info()
                        last_frame = None
                        while exc_traceback is not None:
                            _self = exc_traceback.tb_frame.f_locals.get('self', None)
                            if (_self is not None) and (isinstance(_self, TestListener)):
                                last_frame = exc_traceback.tb_frame
                            # end if
                            exc_traceback = exc_traceback.tb_next
                        # end while

                        if last_frame is None:
                            warn(f'Exception in listener:{exception}', stacklevel=1)
                        else:
                            warn_explicit(f'Exception in listener:{self.listenerFunction.__name__}',
                                          UserWarning,
                                          last_frame.f_code.co_filename,
                                          last_frame.f_lineno,
                                          last_frame.f_globals.get('__name__', 'Unknown'))
                        # end if

                        if propagateException:
                            raise
                        # end if

                    finally:
                        # This is needed to prevent circular references
                        del exc_traceback
                        del last_frame
                    # end try
                    return None
                # end try
            # end def __call__

            def __str__(self):
                """
                Provides information on the wrapped function

                :return: The current object, as a string.
                :rtype: ``str``
                """
                return str(self.listenerFunction)
            # end def __str__

            __repr__ = __str__
        # end class Absorber

        listeners_for_type.add(Absorber(listenerFunction))
    # end def addListener

    # noinspection PyPep8Naming
    def removeListener(self, listenerType, listenerFunction):
        """
        Remove a previously added listener.

        :param listenerType: The type of listener to remove
        :type listenerType: ``int|str``
        :param listenerFunction: The callback function that listens for events.
        :type listenerFunction: ``str``
        """
        listeners_for_type = self._getListeners(listenerType)
        for listenerFunction in [absorber for absorber in listeners_for_type
                                 if absorber.listenerFunction is listenerFunction]:
            listeners_for_type.discard(listenerFunction)
        # end for
    # end def removeListener

    # noinspection PyPep8Naming
    def _getListeners(self, listenerType):
        """
        Obtain  the listeners for a given type

        :param listenerType: Type the listeners are registered to
        :type listenerType: ``int|str``

        :return: listener matching the given type
        :rtype: ``Listener``
        """
        return self.listeners.setdefault(listenerType, set())
    # end def _getListeners

    # noinspection PyPep8Naming
    def startTest(self, test):
        """
        Called when the given test is about to be run

        :param test: The test about to be run.
        :type test: ``Test``
        """
        # Notify listeners
        listeners = self._getListeners(TYPE_START)
        for listener in listeners:
            listener(test)
        # end for

        self.testsRun += 1
    # end def startTest

    # noinspection PyPep8Naming
    def startRun(self, context, resumed):
        """
        Called when a TestRunner is about to start

        :param context: The context in which the tests will run
        :type context: ``Context``
        :param resumed: Flag indicating whether the runner is being resumed.
        :type resumed: ``bool``
        """
        # Notify listeners
        listeners = self._getListeners(TYPE_STARTRUN)
        for listener in listeners:
            listener(context, resumed)
        # end for
    # end def startRun

    # noinspection PyPep8Naming
    def stopRun(self, suspended):
        """
        Called when a TestRunner has been stopped

        :param suspended: Flag indicating whether the runner is being suspended.
        :type suspended: ``bool``
        """
        # Notify listeners
        listeners = self._getListeners(TYPE_STOPRUN)
        for listener in listeners:
            listener(self, suspended)
        # end for
    # end def stopRun

    def log(self, test, level, msg, *args, **kwargs):
        """
        Log a message for the given test.

        :param test: The test for which to log
        :type test: ``Test``
        :param level: The log level
        :type level: ``int``
        :param msg: The message to log
        :type msg: ``str``
        :param args: Positional arguments
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        listeners = self._getListeners(TYPE_LOG)
        for listener in listeners:
            listener(test, level, msg, *args, **kwargs)
        # end for
    # end def log

    # noinspection PyPep8Naming
    def addPerformanceData(self, test, key, value, unit=None):
        """
        Called when the given test wants to add a performance data to the pool.

        :param test: The test for which to log
        :type test: ``Test``
        :param key: Key to add
        :type key: ``str``
        :param value: Value to add
        :type value: ``int,float``
        :param unit: The unit of the traced value - OPTIONAL
        :type unit: ``str``
        """
        # Notify listeners
        listeners = self._getListeners(TYPE_PERFORMANCE)
        for listener in listeners:
            listener(test, key, value, unit)
        # end for
    # end def addPerformanceData

    def add_test_data(self, test, data):
        """
        Called when the given test wants to add a test data to the pool.

        :param test: The test for which to log
        :type test: ``PyHarnessCase``
        :param data: test data string to add to the log
        :type data: ``str``
        """
        # Notify listeners
        listeners = self._getListeners(TYPE_TEST_DATA)
        for listener in listeners:
            listener(test, data)
        # end for
    # end def add_test_data

    # noinspection PyPep8Naming
    def stopTest(self, test):
        """
        Called when the given test has been run

        :param test: The test that terminated.
        :type test: ``Test``
        """
        # Notify listeners
        listeners = self._getListeners(TYPE_STOP)
        for listener in listeners:
            listener(test)
        # end for
    # end def stopTest

    # noinspection PyPep8Naming
    def addResult(self, resultType, test, *data):
        """
        Add a result by type, and notify the relevant listeners

        The data will depend on the result type being added.
        Typically, this will be:
        - An exception info for errors, failures, etc...
        - A string for testcases
        - None for a success, start, stop

        :param resultType:  The result type to add
        :type resultType: ``int``
        :param test: The test to add
        :type test: ``Test``
        :param data: Data relevant to the result type.
        :type data: ``tuple|str|None``
        """
        # Notify listeners
        listeners = self._getListeners(resultType)
        for listener in listeners:
            listener(test, *data)
        # end for

        # Trace data in log, if it is an exception tuple
        if resultType in (TYPE_ERROR, TYPE_FAILURE):
            # data is an __excinfo
            tracelist = format_exception(*(data[0]))
            self.log(test, _LEVEL_ERROR, "\n".join(tracelist))
        # end if

        # Collect result
        results = self.results.setdefault(resultType, [])
        results.append(test.id())
    # end def addResult

    # noinspection PyPep8Naming
    def addError(self, test, err):
        """
        Called when an error has occurred

        :param test: The test that caused the error.
        :type test: ``Test``
        :param err: The error cause
        :type err: ``tuple``
        """
        if sys.version_info >= (3, 11):
            self.errors.append((test, err))
        # end if
        self.addResult(TYPE_ERROR, test, err)
    # end def addError

    # noinspection PyPep8Naming
    def addFailure(self, test, err):
        """
        Called when a failure has occurred

        :param test: The test that caused the failure.
        :type test: ``Test``
        :param err: The failure cause
        :type err: ``tuple``
        """
        if sys.version_info >= (3, 11):
            self.failures.append((test, err))
        # end if
        self.addResult(TYPE_FAILURE, test, err)
    # end def addFailure

    # noinspection PyPep8Naming
    def addExpectedFailure(self, test, err):
        """
        Called when an expected failure has occurred

        :param test: The test that caused the expected failure.
        :type test: ``Test``
        :param err: The expected failure cause
        :type err: ``tuple``
        """
        if sys.version_info >= (3, 11):
            self.expectedFailures.append((test, err))
        # end if
        self.addResult(TYPE_EXP_FAIL, test, err)
    # end def addExpectedFailure

    # noinspection PyPep8Naming
    @failfast
    def addUnexpectedSuccess(self, test):
        """Called when a test was expected to fail, but succeed."""
        self.unexpectedSuccesses.append(test)
    # end def addUnexpectedSuccess

    # noinspection PyPep8Naming
    def addSkip(self, test, err):
        """
        Called when a test is skipped

        :param test: The test that was skipped.
        :type test: ``Test``
        :param err: The skipped cause
        :type err: ``tuple``
        """
        if sys.version_info >= (3, 11):
            self.skipped.append((test, err))
        # end if
        self.addResult(TYPE_SKIPPED, test, err)
    # end def addSkip

    # noinspection PyPep8Naming
    # noinspection PyUnusedLocal
    def addSubTest(self, test, subtest, err):
        """
        Called at the end of a subtest.
        'err' is None if the subtest ended successfully, otherwise it's a
        tuple of values as returned by sys.exc_info().

        :param test: The test which contains subtests.
        :type test: ``TestCase``
        :param subtest: The subtest to add.
        :type subtest: ``str``
        :param err: The error cause
        :type err: ``tuple``
        """
        # By default, we don't do anything with successful subtests, but
        # more sophisticated test results might want to record them.
        if err is not None:
            if getattr(self, 'failfast', False):
                self.stop()
            # end if
            if issubclass(err[0], test.failureException):
                self.addResult(TYPE_FAILURE, test, err)
            else:
                self.addResult(TYPE_ERROR, test, err)
            # end if
        # end if
    # end def addSubTest

    # noinspection PyPep8Naming
    def addSuccess(self, test):
        """
        Called when a test has completed successfully

        :param test: The test that completed
        :type test: ``Test``
        """
        self.addResult(TYPE_SUCCESS, test, None)
    # end def addSuccess

    # noinspection PyPep8Naming
    def addTestCase(self, test, testcase, author=None, comment=None):
        """
        Called when a test has verified a testcase

        :param test: The test that verified the testcase
        :type test: ``Test``
        :param testcase: The testcase that was verified
        :type testcase: ``str``
        :param author: The author of the validation (None if automatic) - OPTIONAL
        :type author: ``str``
        :param comment: A comment on the validation - OPTIONAL
        :type comment: ``str``
        """
        self.addResult(TYPE_TESTCASES, test, testcase, author, comment)
    # end def addTestCase

    # noinspection PyPep8Naming
    def wasSuccessful(self, test=None):
        """
        Tell whether this test was a success.

        :param test: Name of the test
        :type test: ``Test``

        :return: Flag indicating whether the test succeeded.
        :rtype: ``bool``
        """
        problem_types = [TYPE_ERROR, TYPE_FAILURE]

        count = 0
        if test is None:
            # count all results
            for problemType in problem_types:
                count += len(self.results.setdefault(problemType, []))
            # end for
        else:
            # count only results for the test
            test_id = test.id()
            for problemType in problem_types:
                results_for_type = self.results.setdefault(problemType, [])
                count += reduce(lambda x, y: (y == test_id) and x+1 or x, results_for_type, 0)
            # end for
        # end if

        return count == 0
    # end def wasSuccessful

    def stop(self):
        """
        Indicate that the tests should be aborted
        """
        self.shouldStop = 1
    # end def stop

    def __repr__(self):
        errored = len(self.results.setdefault(TYPE_ERROR, []))
        failed = len(self.results.setdefault(TYPE_FAILURE, []))
        skipped = len(self.results.setdefault(TYPE_SKIPPED, []))

        return f"<{self.__class__} run={self.testsRun} errors={errored} failures={failed} skipped={skipped}>"
    # end def __repr__
# end class TestResult


class Test(object):
    """
    Interface definition of a Test

    This class provides a common interface to address tests.
    """

    def __init__(self):
        super().__init__()
        self.warning_occurred = False
    # end def __init__

    def run(self, result, context):
        """
        The run method runs the current test.

        :param result: The collector for the test results.
        :type result: ``TestResult``
        :param context: The context in which the tests will run
        :type context: ``Context``
        """
        raise NotImplementedError()
    # end def run

    def id(self):
        """
        Obtain a (unique) test id.

        This test id is the fully qualified name to the test implementation.

        :return: A test id
        :rtype: ``str``
        """
        raise NotImplementedError()
    # end def id

    # noinspection PyPep8Naming
    def canRun(self, result, context):
        """
        Test whether the test is allowed to run.

        This method defaults to True, always allowing a test to run.
        Note that, depending on the underlying implementation, further methods
        may need to be called to obtain, for instance:
        - The test id
        - Contextual information
        - GUI state

        :param result: The collector for the test results.
        :type result: ``TestResult``
        :param context: The context in which the tests will run
        :type context: ``Context``

        :return: True if the test is allowed to be run, False otherwise.
        :rtype: ``bool``
        """
        return True

    # end def canRun

    # noinspection PyPep8Naming
    def canRunCore(self, result, context):
        """
        Test whether the test is allowed to run, based on the context's filter
        attribute.

        This is useful for providing external, possibly UI-defined filters on
        the tests to run.
        Note that this API CANNOT be merged within the default canRun, as it
        would rely on the canRun overload's proper call of the parent implementation.

        This should be called before canRun, as:
        - The default implementation (no filters) is fast
        - The test-specific implementation may rely on non-available resources.

        :param result: The collector for the test results.
        :type result: ``TestResult``
        :param context: The context in which the tests will run
        :type context: ``Context``

        :return: True if the test is allowed to be run, False otherwise.
        :rtype: ``bool``
        """
        if result.shouldStop:
            return False
        # end if

        if (context is not None) and context.kill:
            return False
        # end if

        if context is not None:
            return context.filter(self, context)
        # end if

        return True
    # end def canRunCore

    # noinspection PyPep8Naming
    def _fixContext(self, context):
        """
        Fix the context, if it does not exist.

        If context is None, a new context is returned. Otherwise, the context is
        returned with no modifications.

        :param context: The pre-existing context
        :type context: ``Context``

        :return: The newly created context, or the existing one if any
        :rtype: ``Context``
        """
        if context is None:

            if self.id().rsplit('.', 1)[-1] not in ('testCaseChecked', 'testCaseManualChecked'):

                root_paths = []
                # noinspection PyBroadException
                try:
                    from pyharness.context import ContextLoader
                    context_loader = ContextLoader()
                    # noinspection PyUnresolvedReferences
                    from pysetup import TESTS_PATH
                    # noinspection PyUnresolvedReferences
                    from pysetup import PROJECT_PATH
                    root_paths = [normpath(join(PROJECT_PATH, '..', TESTS_PATH))]

                    # Also consider the PYTHONPATH root of the current test case
                    module = importFqn(self.__class__.__module__)
                    module_path = module.__file__
                    if module_path is not None:
                        module_path = normpath(module_path.rsplit('.', 1)[0])
                        module_path_tail = self.__class__.__module__.replace('.', sep)
                        if module_path.endswith(module_path_tail):
                            python_path_local_root = module_path[:-len(module_path_tail)]
                            root_paths.append(python_path_local_root)
                        # end if
                    # end if

                    # Also consider elements if sys.path that begin with PROJECT_PATH
                    prefix = normpath(PROJECT_PATH)
                    root_paths.extend([p for p in sys.path if normpath(p).startswith(prefix)])

                    # Lookup from egg dependencies
                    try:
                        # noinspection PyUnresolvedReferences
                        from pysetup import LOADED_EGG_PATHS
                        root_paths.extend(LOADED_EGG_PATHS)
                    except ImportError:
                        pass
                    # end try

                    # Fix duplicates
                    _rootPaths = [normpath(x) for x in root_paths]

                    from os.path import basename
                    from os.path import dirname

                    root_paths = []
                    for rootPath in _rootPaths:
                        if rootPath in root_paths:
                            continue
                        # end if

                        root_path_base_name = basename(rootPath)
                        if (root_path_base_name == 'TESTSUITES') and dirname(rootPath) in root_paths:
                            continue
                        # end if

                        if join(rootPath, 'TESTSUITES') in root_paths:
                            continue
                        # end if

                        root_paths.append(rootPath)
                    # end for

                    context = context_loader.load(root_paths, {})

                except Exception:
                    # The context could not be initialized.
                    # This _may_ be problematic if the test relies on the context
                    # contents. But it may not, if the test does not depend on the
                    # context (A pure TestCase).
                    print(('No context, inspected paths are:\n  %s' % ('\n  '.join(root_paths))))

                    import traceback
                    print((traceback.format_exc()))

                    context = None
                # end try
            # end if
        # end if

        return context
    # end def _fixContext

    # noinspection PyPep8Naming
    @staticmethod
    def _fixResult(result):
        """
        Fix the result, if it does not exist.

        If result is None, a new result is returned. Otherwise, the result is
        returned with no modifications.

        :param result: The pre-existing result.
        :type result: ``TestResult``

        :return: The newly created result, or the existing one if any.
        :rtype: ``TestResult``
        """
        if result is not None:
            return result
        # end if

        return TestResult()
    # end def _fixResult
# end class Test


class TestCase(Test, UnitTestCase):
    """
    A class whose instances are single test cases.

    By default, the test code itself should be placed in a method named
    'runTest'.

    If the fixture may be used for many test cases, create as
    many test methods as are needed. When instantiating such a TestCase
    subclass, specify in the constructor arguments the name of the test method
    that the instance is to execute.

    Test authors should subclass TestCase for their own tests. Construction
    and deconstruction of the test's environment ('fixture') can be
    implemented by overriding the 'setUp' and 'tearDown' methods respectively.

    If it is necessary to override the __init__ method, the base class
    __init__ method must always be called. It is important that subclasses
    should not change the signature of their __init__ method, since instances
    of the classes are instantiated automatically by parts of the framework
    in order to be run.

    IMPORTANT: Cooperative multiple inheritance IS NOT recommended for these classes,
    as it ultimately inherits from unittest.TestCase, which breaks the super
    implementation.
    """

    # __implements__ = Test

    # This attribute determines which exception will be raised when
    # the instance's assertion methods fail; test methods raising this
    # exception will be deemed to have 'failed' rather than 'errored'
    failureException = AssertionError

    # Threadlocal data, used to contain lock information, for exclusion between
    # test runs
    THREAD_LOCAL_DATA = local()

    ALLOWED_LEVELS = frozenset(_ALL_LEVELS)

    # noinspection PyPep8Naming
    def __init__(self, methodName='runTest'):
        """
        Create an instance of the class that will use the named test method when
        executed.

        :param methodName: The named test method to run.
        :type methodName: ``str``

        :raise ``ValueError``: If the instance does not have a method with the specified name.
        """
        Test.__init__(self)
        UnitTestCase.__init__(self, methodName=methodName)

        try:
            test_method = getattr(self, methodName)
        except AttributeError:
            raise ValueError(f"No such test method in {self.__class__}: {methodName}")
        # end try

        self._testMethodDoc = test_method.__doc__
        self._testMethodName = methodName
        self.__result = None
        self.debugSubTests = False
        self.__checkedTestCases = None
        self._outcome = None

        self._currentContext = None
        self._fixtures = []
        self.status = None
    # end def __init__

    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        UnitTestCase.setUp(self)
    # end def setUp

    def tearDown(self):
        """
        Hook method for deconstructing the test fixture after testing it.
        """
        UnitTestCase.tearDown(self)
    # end def tearDown

    def countTestCases(self):
        """
        Count the number of test cases in this class

        :return: Number of tests
        :rtype: ``int``
        """
        return 1
    # end def countTestCases

    def shortDescription(self):
        """
        Return a one-line description of the test, or None if no description has been provided.

        The default implementation of this method returns the first line of the specified test method's docstring.

        :return: A one-line description of the test.
        :rtype: ``str``
        """
        return self.fullDescription().split('\n')[0].strip()
    # end def shortDescription

    def fullDescription(self):
        """
        Obtain the full description (the full docstring) of the test.

        :return: Description mode
        :rtype: ``str``
        """
        if self._testMethodDoc is None:
            return ''
        # end if

        return self._testMethodDoc.strip()
    # end def fullDescription

    def id(self):
        """
        NB: This test id is only based on the class and method names.
        """
        return f"{self.__class__.__module__}.{self.__class__.__name__}.{self._testMethodName}"
    # end def id

    def short_name(self):
        """
        Obtain the short name of the test based only on the class and method names.

        :return: Short name
        :rtype: ``str``
        """
        return f"{self.__class__.__name__}.{self._testMethodName}"
    # end def short_name

    def __str__(self):
        return f"{self._testMethodName} ({self.__class__.__module__}.{self.__class__.__name__})"
    # end def __str__

    def __repr__(self):
        return f"<{self.__class__.__module__}.{self.__class__.__name__} testMethod={self._testMethodName}>"
    # end def __repr__

    def canRun(self, result, context):
        # See ``pyharness.core.Test.canRun``
        # Are the features attached to the test case all enabled
        result = result and (self.is_runnable(features, result, context))
        if result is not False:
            # Are the services attached to the test case all available
            result = result and (self.is_runnable(services, result, context))
            if result is not False:
                # Is there a known bug triggering an expected failure
                expecting_failure = self.is_runnable(items=bugtracker, result=None, context=context,
                                                     all_result_true=False)
                if expecting_failure:
                    # Call equivalent to @unittest.expectedFailure
                    unittest.expectedFailure(self)
                # end if
            # end if
        # end if
        return result
    # end def canRun

    def is_runnable(self, items, result, context, all_result_true=True):
        """
        Test whether the items decorator allow to run the test
        """
        f = getattr(self, self._testMethodName)
        for (function_feature, args) in items.getFeatures(f):
            if not isFeatureReversed(function_feature):
                base_feature = function_feature[:]
            else:
                base_feature = function_feature[len(REVERSED_MARK):]
            # end if

            if base_feature not in items._decoratorToFeatures:
                result = False
                if hasattr(items, '_false_decorators'):
                    items._false_decorators.append((f, base_feature))
                    continue
                else:
                    break
                # end if
            # end if

            checker = items._decoratorToFeatures[base_feature]
            checker_result = checker(context, *(list(args)))
            checker_result = not checker_result if isFeatureReversed(function_feature) else checker_result
            if all_result_true:
                result = checker_result if result is None else result and checker_result
            else:
                result = checker_result if result is None else result or checker_result
            # end if

            if (not result and all_result_true) or (result and not all_result_true):
                if hasattr(items, '_false_decorators'):
                    if not checker_result:
                        items._false_decorators.append((f, base_feature))
                    # end if
                else:
                    break
                # end if
            # end if
        # end for
        return result
    # end def is_runnable

    def run(self, result=None, context=None):
        # See ``pyharness.core.Test.run``
        return self(result, context)
    # end def run

    def __setUpContext(self, result, context):
        """
        Set up the context, for easy access from the test methods.

        This works by injecting proxy methods for all getters of the context
        object

        :param result:The result for which the context is set up
        :type result: ``TestResult|None``
        :param context: The context tp provide access to.
        :type context: ``Context``

        Warning This introduces a state to the testcase, and will probably break if tests are run concurrently

        :raise ``AttributeError``: If the context is already initialized
        """
        self.__result = result

        if self._currentContext is not None:
            raise AttributeError("Context already initialized")
        # end if
        self._currentContext = context
    # end def __setUpContext

    # noinspection PyUnusedLocal
    def __tearDownContext(self, unused, context):
        """
        Remove access to the getters from the context in the current class.

        :param unused: The result for which the context is torn down
        :type unused: ``TestResult|None``
        :param context: The context to detach from the current object.
        :type context: ``Context``

        :raise ``AttributeError``: If the context is already cleared
        """
        if context is not None:
            if self._currentContext is None:
                raise AttributeError("Context already cleared")
            # end if
            self._currentContext = None
        # end if

        self.__result = None
    # end def __tearDownContext

    def _getRootContext(self):
        """
        Get root context

        :return: Root context
        :rtype: ``RootContext``
        """
        tmp_context = self._currentContext
        last_context = None
        while not (last_context is not None and last_context == tmp_context):
            last_context = tmp_context
            tmp_context = tmp_context.getParent()
        # end while
        return tmp_context
    # end def _getRootContext

    def __abortIfNeeded(self):
        """
        Check whether the current test must be aborted
        """
        if self._currentContext is not None:
            context = self._getRootContext()
            if context is not None and context.abort:
                raise AssertionError("Aborted")
            # end if
        # end if
    # end def __abortIfNeeded

    def getContext(self):
        """
        Obtain  the context for the current test.

        :return: The context for the current test.
        :rtype: ``Context``
        """
        return self._fixContext(self._currentContext)
    # end def getContext

    def pushContext(self, mode=None, product=None, variant=None, target=None):
        """
        Creates a new context, derived from the current one, and replace the
        current context by the new one.

        The previous context is restored by calling @c popContext

        :param mode: The mode of the new context - OPTIONAL
        :type mode: ``str``
        :param product: The product of the new context - OPTIONAL
        :type product: ``str``
        :param variant: The variant of the new context - OPTIONAL
        :type variant: ``str``
        :param target: The target of the new context - OPTIONAL
        :type target: ``str``
        """
        context_loader = importFqn("pyharness.context.ContextLoader")
        new_context = context_loader().deriveContext(
            self._currentContext, mode=mode, product=product, variant=variant, target=target)
        new_context.setParent(self._currentContext)

        # Increase ressources counters for new context
        for _, device in getattr(new_context, '_AContext__smartDevices'):
            if device.is_allocated():
                device.allocate()
            # end if
        # end for

        for _, debugger in getattr(new_context, '_AContext__debuggers'):
            if debugger.isOpen():
                debugger.open()
            # end if
        # end for

        self._currentContext = new_context
    # end def pushContext

    def popContext(self):
        """
        Restores a previously pushed context
        """
        tmp_context = self._currentContext.parent
        del self._currentContext
        self._currentContext = tmp_context
    # end def popContext

    def log(self, level, msg, *args, **kwargs):
        """
        Log the given message.

        :param level: The level at which the message is logged
        :type level: ``int``
        :param msg: The message to log
        :type msg: ``str``
        :param args: Positional arguments
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        if not (self.__result is None):
            if hasattr(self.__result, 'log') and (level in self.ALLOWED_LEVELS or (level & _MASK_ALWAYS)):
                self.__result.log(self, level, msg, *args, **kwargs)
            # end if

        # end if
        self.__abortIfNeeded()
    # end def log

    def addPerformanceData(self, key, value, unit=None):
        """
        Add performance data for the specified key.

        This is a very generic way to collect performance data on generic events.
        Not that it is possible to collect multiple performance data for any one
        key.

        A typical use for this API would be to log the time spent in several
        functions, or the time spent waiting on a particular IO.

        :param key: The key that identified this performance data.
                    This is usually a string, such as a label, address, or name
        :type key: ``str``
        :param value: The value associated with this performance data.
        :type value: ``int|float``
        :param unit: The unit of the traced value - OPTIONAL
        :type unit: ``str``
        """
        if not (self.__result is None) and hasattr(self.__result, "addPerformanceData"):
            self.__result.addPerformanceData(self, key, value, unit)
        # end if

        self.__abortIfNeeded()
    # end def addPerformanceData

    def add_test_data(self, data):
        """
        This is a very generic way to collect test data on generic events.

        A typical use for this API would be to log the random generated keys, mouse buttons, etc.

        :param data: Test data string to add to the log
        :type data: ``str``
        """
        if not (self.__result is None):
            if hasattr(self.__result, "add_test_data"):
                self.__result.add_test_data(self, data)
            # end if
        # end if

        self.__abortIfNeeded()
    # end def add_test_data

    # noinspection PyPep8Naming
    def checkTestCase(self, testCase, author=None, comment=None):
        """
        Check a TestCase as validated

        :param testCase: The TestCase to validate.
        :type testCase: ``str``
        :param author: The author of the validation (None if automatic) - OPTIONAL
        :type author: ``str``
        :param comment: A comment on the validation - OPTIONAL
        :type comment: ``str``
        """
        if not (self.__result is None):
            # Check that the caller is either a method from the current class,
            # beginning with test
            # noinspection PyBroadException
            try:
                # noinspection PyUnresolvedReferences
                caller_name = sys._getframe(1).f_code.co_name
            except Exception:
                caller_name = None
            # end try

            assert ((caller_name is None) or
                    (caller_name in ('checkTestCase', 'checkTestCaseManual',
                                     'testCaseChecked', 'testCaseManualChecked')) or
                    (caller_name.startswith('test') and hasattr(self, caller_name)) or
                    (caller_name.startswith('subTest') and hasattr(self, caller_name))), \
                f'The checkTestCase and checkTestCaseManual APIs must be called from the test (found: {caller_name})'

            assert testCase not in self.__checkedTestCases, 'A testCase must be checked at most ONCE per test'
            self.__checkedTestCases.add(testCase)
            if hasattr(self.__result, 'addTestCase'):
                self.__result.addTestCase(self, testCase, author, comment)
            # end if

        # end if
        self.__abortIfNeeded()
    # end def checkTestCase

    testCaseChecked = checkTestCase

    # noinspection PyPep8Naming
    def checkTestCaseManual(self, testCase, shortText=None, longText=None):
        """
        Check a manual testCase.
        Depending on the environment implementation, this may either
        raise a failure, (No user UI available), or ask the user for
        confirmation.

        :param testCase: The TestCase to validate.
        :type testCase: ``str``
        :param shortText: A one-line explanation of the TestCase - OPTIONAL
        :type shortText: ``str``
        :param longText: A longer, multi-line explanation of the TestCase - OPTIONAL
        :type longText: ``str``
        """
        author = ''
        context = self.getContext()
        manual_test_case_ui = context.manualTestCaseUi
        comment = ''
        if manual_test_case_ui is not None:
            status, author, comment = context.manualTestCaseUi(testCase, shortText, longText)
        else:
            status = False
        # end if

        if not status:
            msg = 'Manual TestCase failed: %s' % testCase
            if comment:
                msg += ': %s' % comment
            # end if
            self.fail(msg)
        else:
            self.testCaseChecked(testCase, author, comment)
        # end if

        self.__abortIfNeeded()
    # end def checkTestCaseManual

    testCaseManualChecked = checkTestCaseManual

    def subTestRunner(self):
        """
        A dummy implementation of the subTestRunner.

        This implementation MUST NOT be overridden by derived classes.
        It always generates an error, as it should never be called.
        """
        raise RuntimeError('The subTestRunner is never called directly.')
    # end def subTestRunner

    # noinspection PyPep8Naming
    def _getInstanceAttrNames(self, attrNames):
        """
        Remove class attribute names from attrNames

        :param attrNames: List of attributes
        :type attrNames: ``list``

        :return: attrNames without class attributes names
        :rtype: ``list``
        """
        # Remove instance attributes that are different from the None-Initialized class attribute
        class_names = dir(self.__class__)

        updated_names = set([name for name in class_names if (
                getattr(self.__class__, name) is None and getattr(self, name) is not getattr(self.__class__, name))])
        result = attrNames | updated_names

        class_names = set(dir(TestCase))
        result -= class_names
        return result
    # end def _getInstanceAttrNames

    def __call__(self, result=None, context=None):
        """
        Run the test.

        This method is the equivalent of E. Gamma's runTest method.

        An additional, automatic cleanup is performed on the test instance:
        - instance variables newly created during the setUp are detected
        - those instance variables are erased after tearDown

        :param result: The test result used to collect test runs.
        :type result: ``TestResult``
        :param context: The context in which to call the tests.
        :type context: ``Context``
        """
        # Create inner instances of result and context, if none are found.
        # It is time-consuming, but allows PyHarness's tests to run within pyunit
        result = self._fixResult(result)
        context = self._fixContext(context)

        test_methods = self.__extractMethods(context)

        if len(test_methods) == 0 or (not self.canRunCore(result, context)) or (not self.canRun(result, context)):
            return
        # end if

        # Prevent two instances of the same test to run concurrently
        # This is only done for actual runs.
        if context is None or not context.collectOnly():
            self.__acquireConcurrentRun()
        # end if

        try:
            if len(test_methods) > 0:
                result.startTest(self)

                try:
                    # If the test must only be collected, do not perform
                    # setUp/run/tearDown
                    if context is None or not context.collectOnly():

                        # Handle tests tagged with @monothread
                        count_to_lock = self.__acquireThreadLimit(test_methods)
                        try:
                            # Run the setUp
                            is_run_ok = TYPE_SUCCESS
                            pre_setup_names = set(dir(self))
                            set_up_ok = self.__runSetup(result, context)

                            if set_up_ok and self._outcome.success:
                                self.__checkedTestCases = set()
                                # ---------------
                                #  Class fixtures
                                # ---------------
                                # Apply class fixtures defined in the class setup
                                # through a self.addFixture() call
                                self.doFixtures()
                                # ---------------
                                # Apply class fixtures decorating the class:
                                # @fixtures()
                                if fixtures.isClassDecorated(self.__class__):
                                    for function, args, kwargs in fixtures.getClassFixtures(self.__class__):
                                        with self._outcome.testPartExecutor(self):
                                            function(self, *args, **kwargs)
                                        # end with
                                    # end for
                                # end if
                                # ---------------

                                # Run the actual tests
                                is_run_ok = self.__runTestMethods(result, test_methods)

                                self.__checkedTestCases = None

                                names_to_cleanup = set(dir(self))
                                names_to_cleanup = self._getInstanceAttrNames(names_to_cleanup - pre_setup_names)

                                # Run the tearDown
                                self.__runTearDown(result, context, names_to_cleanup, is_run_ok)
                            # end if
                            if not (is_run_ok == TYPE_SKIPPED):
                                # ---------------
                                #  CleanUps
                                # ---------------
                                # Apply cleanup defined in the class setup or directly in the test
                                # through a self.addCleanup() call.
                                self.doCleanups()
                            # end if
                            if sys.version_info < (3, 11):
                                for test, reason in self._outcome.skipped:
                                    # skipTest called directly in the test case
                                    self._addSkip(result, test, reason)
                                # end for
                                # noinspection PyUnresolvedReferences
                                self._feedErrorsToResult(result, self._outcome.errors)
                            # end if
                            if self._outcome.success:
                                if self._outcome.expecting_failure:
                                    if self._outcome.expectedFailure:
                                        # noinspection PyUnresolvedReferences
                                        self._addExpectedFailure(result, self._outcome.expectedFailure)
                                    else:
                                        # noinspection PyUnresolvedReferences
                                        self._addUnexpectedSuccess(result)
                                    # end if
                                    self._outcome.expecting_failure = False
                                # end if
                            # end if
                        finally:
                            # Unblock other waiting tests
                            self.__releaseThreadLimit(count_to_lock)
                        # end try
                    elif context is not None and context.collectOnly():
                        pass
                    # end if
                finally:
                    if len(test_methods) > 0:
                        result.stopTest(self)
                    # end if
                # end try
            # end if
        finally:
            # Unblock other instances of the same test
            # This is only done for actual runs.
            if context is None or not context.collectOnly():
                self.__releaseConcurrentRun()
            # end if
        # end try
    # end def __call__

    def debug(self, context=None):
        """
        Run the test without collecting errors in a TestResult

        :param context: The context in which the test is run.
        :type context: ``Context``
        """
        self.__setUpContext(None, context)

        self.setUp()
        getattr(self, self._testMethodName)()
        self.tearDown()

        self.__tearDownContext(None, context)
    # end def debug

    @staticmethod
    def __exc_info():
        """
        Return a version of sys.exc_info() with the traceback frame minimized;

        Usually the top level of the traceback frame is not needed, as it only
        contains internal, pyharness-specific information.

        :return: Tuple
        :rtype: ``typle``
        """
        exception_type, exception_value, tb = sys.exc_info()
        if sys.platform[:4] == 'java':  # tracebacks look different in Jython
            return exception_type, exception_value, tb
        # end if
        new_traceback = tb.tb_next
        if new_traceback is None:
            return exception_type, exception_value, tb
        # end if

        return exception_type, exception_value, new_traceback
    # end def __exc_info

    # noinspection PyMethodOverriding
    @staticmethod
    def fail(msg=None):
        """
        Fail immediately, with the given message.

        :param msg: The failure reason
        :type msg: ``str``
        """
        raise TestException(TYPE_FAILURE, msg)
    # end def fail

    @staticmethod
    def failIf(expr, msg=None):
        """
        Fail the test if the expression is true.

        :param expr: The expression to check
        :type expr: ``bool|None``
        :param msg: The failure reason
        :type msg: ``str``
        """
        if expr:
            raise TestException(TYPE_FAILURE, msg)
        # end if
    # end def failIf

    @staticmethod
    def failUnless(expr, msg=None):
        """
        Fail the test unless the expression is true.

        :param expr: The expression to check
        :type expr: ``bool|None``
        :param msg: The failure reason - OPTIONAL
        :type msg: ``str``
        """
        if not expr:
            raise TestException(TYPE_FAILURE, msg)
        # end if
    # end def failUnless

    # noinspection PyPep8Naming
    @staticmethod
    def assertRaises(excClass, callableObj, *args, **kwargs):
        """
        Fail unless an excClass exception is thrown by callableObj when
        invoked with arguments args and keyword arguments kwargs.

        If a different type of exception is thrown, it will not be caught, and
        the test case will be deemed to have suffered an error, exactly as for
        an unexpected exception.

        :param excClass: The exception class to check
        :type excClass: ``Exception``
        :param callableObj: The callable object to check
        :type callableObj: ``callable``
        :param args: Positional arguments
        :type args: ``tuple``
        :param kwargs: Keyword arguments
        :type kwargs: ``dict``
        """
        # noinspection PyBroadException
        try:
            callableObj(*args, **kwargs)
        except excClass:
            pass
        else:
            if hasattr(excClass, '__name__'):
                exc_name = excClass.__name__
            else:
                exc_name = str(excClass)
            # end if
            raise TestException(TYPE_FAILURE, f"Exception {exc_name} should have been raised")
        # end try
    # end def assertRaises

    # noinspection PyPep8Naming
    @staticmethod
    def assertEqual(expected, obtained, msg=None, maxDisplayLength=2048):
        """
        Fail if the two objects are unequal as determined by the
        '!=' operator.

        :param expected: The expected element to compare
        :type expected: ``object``
        :param obtained: The obtained element to compare
        :type obtained: ``object``
        :param msg: The message to display in case of error - OPTIONAL
        :type msg: ``str``
        :param maxDisplayLength: The maximum display length for the comparison - OPTIONAL
        :type maxDisplayLength: ``int``
        """
        # This MUST NOT be replaced by (expected != obtained), as this
        # invokes __ne__ instead of __eq__
        if not (expected == obtained):
            if not isinstance(expected, str):
                str1 = str(expected)
            else:
                str1 = expected
            # end if

            if not isinstance(obtained, str):
                str2 = str(obtained)
            else:
                str2 = obtained
            # end if

            str1_trailer = ""
            str2_trailer = ""
            if maxDisplayLength > 0:
                if len(str1) > maxDisplayLength:
                    str1_trailer = "..."
                    str1 = str1[:maxDisplayLength]
                # end if

                if len(str2) > maxDisplayLength:
                    str2_trailer = "..."
                    str2 = str2[:maxDisplayLength]
                # end if
            # end if

            # Compute the offset after which the data differ
            # noinspection PyUnusedLocal
            offset = 0

            max_ind = min(len(str1), len(str2))
            for ind in range(max_ind):
                if str1[ind] != str2[ind]:
                    offset = ind
                    break
                # end if
            else:
                offset = max_ind
            # end for
            caret = "-" * offset

            raise TestException(TYPE_FAILURE, (msg and """%s
                expected: %s%s
                obtained: %s%s
                          %s^""" % (msg, str1, str1_trailer, str2, str2_trailer, caret)) or
                """ expected: %s%s
                obtained: %s%s
                          %s^""" % (str1, str1_trailer, str2, str2_trailer, caret))
        # end if
    # end def assertEqual

    @staticmethod
    def assertNone(obtained, msg=None):
        """
        Fail if the object is not None.

        :param obtained: The element to compare against None
        :type obtained: ``object``
        :param msg: The message to display in case of error - OPTIONAL
        :type msg: ``str``
        """
        if not (obtained is None):
            raise TestException(TYPE_FAILURE, msg and """%s
                expected: None
                obtained: %.2048s""" % (msg, obtained) or """
                expected: None
                obtained: %.2048s""" % obtained)
        # end if
    # end def assertNone

    @classmethod
    def assertTrue(cls, expr, msg=None):
        """
        Fail if ``expr`` is not True.

        Note that this behavior differs from unittest.TestCase.assertTrue,
        which accepts non-zero, non-empty lists and other expressions.

        This method REQUIRES that @c expr be the exact True value

        :param expr: The value to compare
        :type expr: ``bool``
        :param msg: The message to display in case of error - OPTIONAL
        :type msg: ``str``
        """
        if expr is not True:
            msg = (msg + '\n') if msg is not None else ''
            message = '%s\n expected: True\n obtained: %.2048s' % (msg, expr)
            raise TestException(TYPE_FAILURE, message)
        # end if
    # end def assertTrue

    @classmethod
    def assertFalse(cls, expr, msg=None):
        """
        Fail if @c expr is not False.

        Note that this behavior differs from unittest.TestCase.assertFalse,
        which accepts zero, empty lists and other expressions.

        This method REQUIRES that @c expr be the exact False value

        :param expr: The value to compare
        :type expr: ``bool``
        :param msg: The message to display in case of error - OPTIONAL
        :type msg: ``str``
        """
        if expr is not False:
            msg = (msg + '\n') if (msg is not None) else ''
            message = '%s\n expected: False\n obtained: %.2048s' % (msg, expr)
            raise TestException(TYPE_FAILURE, message)
        # end if
    # end def assertFalse

    @staticmethod
    def assertNotNone(obtained, msg=None):
        """
        Fail if the object is None.

        :param obtained: The element to compare against None
        :type obtained: ``object``
        :param msg: The message to display in case of error - OPTIONAL
        :type msg: ``str``
        """
        if obtained is None:
            raise TestException(TYPE_FAILURE, msg and """%s
                obtained: None""" % msg or """obtained: None""")
        # end if
    # end def assertNotNone

    # noinspection PyMethodOverriding
    @staticmethod
    def assertNotEqual(unexpected, obtained, msg=None):
        """
        Fail if the two objects are equal as determined by the '==' operator.

        :param unexpected: The expected element to compare
        :type unexpected: ``Any``
        :param obtained: The obtained element to compare
        :type obtained: ``Any``
        :param msg: The message to display in case of error.
        :type msg: ``str``
        """
        if unexpected == obtained:
            raise TestException(TYPE_FAILURE, msg and """%s obtained: %.2048s""" % (msg, obtained) or
                                """obtained: %.2048s""" % obtained)
        # end if
    # end def assertNotEqual

    failUnlessNone = assertNone

    failIfNone = assertNotNone

    failUnlessEqual = assertEquals = assertEqual

    failIfEqual = assertNotEquals = assertNotEqual

    # failUnlessRaises = assertRaises

    assert_ = failUnless

    TRACEBACK_CODENAMES = ["failUnlessNone", "assertNone", "failIfNone", "assertNotNone", "failUnlessEqual",
                           "assertEquals", "assertEqual", "failIfEqual", "assertNotEquals", "assertNotEqual",
                           "failUnlessRaises", "assertRaises", "assertMutes", "failUnless", "assertTrue",
                           "assertFalse", "assert_", "fail"]

    SYNCHRONIZATION_LOCK = RLock()
    __CONCURRENT_LOCKS = {}

    def __acquireConcurrentRun(self):
        """
        Force only one instance of a test at one time.

        This prevents problems when:
        - More than one thread runs the tests
        - More than one run of the test is schedules.

        Running two instances of the same test is forbidden, as most loggers
        are not designed to work that way (i.e. write the same log file twice)
        """
        with self.SYNCHRONIZATION_LOCK:
            test_id = self.id()

            # The same lock is multiplied by the number of pending tests.
            # This allows locks to be garbage collected once they are not used anymore.
            locks = self.__CONCURRENT_LOCKS.setdefault(test_id, [])
            if len(locks) == 0:
                lock = Lock()
            else:
                lock = locks[0]
            # end if
            locks.append(lock)
        # end with

        lock.acquire()
    # end def __acquireConcurrentRun

    def __releaseConcurrentRun(self):
        """
        Allow other instances of the same test to run.

        This is symmetric to __acquireConcurrentRun
        """
        with self.SYNCHRONIZATION_LOCK:
            test_id = self.id()
            locks = self.__CONCURRENT_LOCKS[test_id]
            lock = locks[0]
            lock.release()
            del locks[0]
        # end with
    # end def __releaseConcurrentRun

    # noinspection PyPep8Naming
    @synchronized(SYNCHRONIZATION_LOCK)
    def __acquireThreadLimit(self, testMethods):
        """
        Block the current test until the number of testrunner threads is lower
        than the maximum allowed for this test.

        :param testMethods: The test methods for this test.
        :type testMethods: ``tuple|list``

        :return: The number of times the lock has been acquired
        :rtype: ``int``
        """
        # The minimum thread count of all methods is used
        min_thread_count = None

        thread_local_data = self.THREAD_LOCAL_DATA

        # This ensures that a non-monothread-tagged test waits for
        if hasattr(thread_local_data, "maxThreadCount"):
            min_thread_count = thread_local_data.maxThreadCount - 1
        # end if

        for _testMethod in testMethods:
            test_limit = monothread.getThreadLimit(_testMethod)
            if min_thread_count is None:
                min_thread_count = test_limit
            elif test_limit is not None and (test_limit < min_thread_count):
                min_thread_count = test_limit
            # end if
        # end for

        count_to_lock = 0
        if hasattr(thread_local_data, "maxThreadCount"):
            if min_thread_count is None:
                count_to_lock = 1
            else:
                count_to_lock = thread_local_data.maxThreadCount - min_thread_count
            # end if
        # end if
        for _ in range(count_to_lock):
            thread_local_data.maxThreadLock.acquire()
        # end for
        return count_to_lock
    # end def __acquireThreadLimit

    # noinspection PyPep8Naming
    def __releaseThreadLimit(self, lockedCount):
        """
        Releases the locks acquired by the current test run.

        :param lockedCount: The number of times the lock has been acquired.
        :type lockedCount: ``int``
        """
        # Finally, release the locked items
        thread_local_data = self.THREAD_LOCAL_DATA
        for _ in range(lockedCount):
            thread_local_data.maxThreadLock.release()
        # end for
    # end def __releaseThreadLimit

    def __extractMethods(self, context):
        """
        Extract a list of methods to run.

        This will return:
        - For 'normal' test cases, the current method to test.
        - For subTestrunner, the list of subTest methods

        :param context: The context that provides:
                        - The filters to apply
                        - Whether collecOnly is True
        :type context: ``Context``

        :return: A list of methods to run between setUp and tearDown
        :rtype: ``list``
        """
        backed_up_test_method_name = None
        backed_up_test_method_doc = None
        # This handles sub-testrunners, i.e. a single test, that launches all

        # methods starting with subTest
        if self._testMethodName == 'subTestRunner':
            test_methods = []
            for x in dir(self):
                if x.startswith(TestLoader.subTestMethodPrefix):
                    if (x != 'subTestRunner') and (x != 'subTest'):
                        test_methods.append(getattr(self, x))
                    # end if
                # end if
            # end for
            try:
                backed_up_test_method_name = self._testMethodName
                backed_up_test_method_doc = self._testMethodDoc
                new_test_methods = []
                for testMethod in test_methods:
                    self._testMethodName = testMethod.__name__
                    self._testMethodDoc = testMethod.__doc__
                    if context is None or context.filter(self):
                        new_test_methods.append(testMethod)
                    # end if
                # end for

                test_methods = new_test_methods
            finally:
                self._testMethodName = backed_up_test_method_name
                self._testMethodDoc = backed_up_test_method_doc
            # end try

            # If we only collect the results, only the subTestRunner is obtained
            if (context is not None and context.collectOnly()) and (len(test_methods) > 0):
                test_methods = (getattr(self, self._testMethodName),)
            # end if

        elif self._testMethodName in ('testCaseChecked', 'testCaseManualChecked'):
            # Filter out the methods reserved by PyHarness
            test_methods = []
        else:
            test_methods = (getattr(self, self._testMethodName),)
        # end if

        return test_methods
    # end def __extractMethods

    # noinspection PyPep8Naming
    def __collectTestMethods(self, result, testMethods):
        """
        Collect the test methods.

        This is similar to __runTestMethods, but does not run the actual methods.

        :param result: The TestResult collector
        :type result: ``TestResult``
        :param testMethods: The list of actual methods to run.
        :type testMethods: ``tuple``
        """
        backed_up_test_method_name = None
        backed_up_test_method_doc = None

        for testMethod in testMethods:
            try:
                backed_up_test_method_name = self._testMethodName
                backed_up_test_method_doc = self._testMethodDoc
                if testMethod.__name__.startswith(TestLoader.subTestMethodPrefix):
                    self._testMethodName = testMethod.__name__
                    self._testMethodDoc = testMethod.__doc__
                    result.startTest(self)
                    result.stopTest(self)
                # end if
            finally:
                self._testMethodDoc = backed_up_test_method_doc
                self._testMethodName = backed_up_test_method_name
            # end try
        # end for
    # end def __collectTestMethods

    def __runSetup(self, result, context):
        """
        Run the setUp of the test, handling any errors.

        :param result: The TestResult collector
        :type result: ``TestResult``
        :param context: The context in which to run
        :type context: ``Context``

        :return: Flag indicating whether the setUp is Ok
        :rtype: ``bool``
        """
        set_up_ok = True

        names_to_cleanup = set()
        # noinspection PyBroadException
        try:
            self.__setUpContext(result, context)
            # Detect names that have appeared during the setUp
            pre_setup_names = set(dir(self))

            self._outcome = _Outcome(result)

            with self._outcome.testPartExecutor(self):
                self.setUp()
            # end with

            if not self._outcome.success:
                set_up_ok = False
                # call tearDown when an exception is caught on setUp()
                with self._outcome.testPartExecutor(self):
                    self.tearDown()
                # end with
            # end if

            post_setup_names = set(dir(self))
            names_to_cleanup = self._getInstanceAttrNames(post_setup_names - pre_setup_names)

        except Exception:
            result.addError(self, self.__exc_info())

            # Delete names that have appeared during the setUp
            for name in names_to_cleanup:
                delattr(self, name)
            # end for
        # end try

        return set_up_ok
    # end def __runSetup

    # noinspection PyPep8Naming
    def __runTestMethods(self, result, testMethods):
        """
        Run the actual test methods.

        :param result: The TestResult collector
        :type result: ``TestResult``
        :param testMethods: The list of actual methods to run.
        :type testMethods: ``tuple|list``

        :return: True of none of the methods failed or errored.
        :rtype: ``bool``
        """
        backed_up_test_method_name = None
        backed_up_test_method_doc = None

        ok = TYPE_ERROR
        previous_failed = 0
        for test_method in testMethods:
            # noinspection PyUnusedLocal
            ok = TYPE_ERROR
            try:
                backed_up_test_method_name = self._testMethodName
                backed_up_test_method_doc = self._testMethodDoc
                if test_method.__name__.startswith(TestLoader.subTestMethodPrefix):
                    self._testMethodName = test_method.__name__
                    self._testMethodDoc = test_method.__doc__
                    result.startTest(self)
                # end if

                self.__abortIfNeeded()

                # This is for DEBUG purposes only, and MUST NOT be activated
                # in RELEASED tests.
                if self.debugSubTests:
                    previous_failed = 0
                # end if

                if previous_failed == 0:
                    # testMethod()
                    test_method = getattr(self, self._testMethodName)
                    if (getattr(self.__class__, "__unittest_skip__", False) or
                            getattr(test_method, "__unittest_skip__", False)):
                        # If the class or method was skipped.
                        try:
                            skip_why = (getattr(self.__class__, '__unittest_skip_why__', '')
                                        or getattr(test_method, '__unittest_skip_why__', ''))
                            if sys.version_info < (3, 11):
                                self._addSkip(result, self, skip_why)
                            else:
                                # call skipTest from TestResult
                                result.addSkip(self, skip_why)
                            # end if
                            ok = TYPE_SKIPPED
                        finally:
                            pass
                        # end try
                        return ok
                    # end if
                    expecting_failure_method = getattr(test_method,
                                                       "__unittest_expecting_failure__", False)
                    expecting_failure_class = getattr(self,
                                                      "__unittest_expecting_failure__", False)
                    expecting_failure = expecting_failure_class or expecting_failure_method

                    # Execute the fixtures
                    if fixtures.isDecorated(test_method):
                        for function, args, kwargs in fixtures.getFixtures(test_method):
                            with self._outcome.testPartExecutor(self):
                                function(self, *args, **kwargs)
                            # end with
                        # end for
                    # end if

                    # Execute the test method
                    self._outcome.expecting_failure = expecting_failure
                    with self._outcome.testPartExecutor(self):
                        test_method()
                    # end with
                    if self._outcome.success:
                        ok = TYPE_SUCCESS
                    else:
                        ok = TYPE_FAILURE
                    # end if

                elif previous_failed == 1:
                    raise TestException(TYPE_FAILURE, message_text='Failed due to a previous sub-test failure')
                else:
                    raise Exception('Error due to a previous sub-test failure')
                    # end if
                # end if

            finally:
                if test_method.__name__.startswith(TestLoader.subTestMethodPrefix):
                    if previous_failed == 0:
                        result.addSuccess(self)
                    # end if
                    result.stopTest(self)
                # end if
                self._testMethodDoc = backed_up_test_method_doc
                self._testMethodName = backed_up_test_method_name
            # end try
        # end for
        return ok
    # end def __runTestMethods

    # noinspection PyPep8Naming
    def __runTearDown(self, result, context, namesToCleanup, ok):
        """
        Run the tearDown method

        :param result: The TestResult collector
        :type result: ``TestResult``
        :param context: The context in which ro run.
        :type context: ``Context``
        :param namesToCleanup: The instance attributes to remove.
        :type namesToCleanup: ``list``
        :param ok: Flag indicating whether the previous run was Ok or not.
        :type ok: ``bool``
        """
        self.status = ok
        # noinspection PyBroadException
        try:
            with self._outcome.testPartExecutor(self):
                self.tearDown()
            # end with

            # Delete names that have appeared during the setUp
            for name in namesToCleanup:
                # Guard against explicit deletions in tearDown
                if hasattr(self, name):
                    delattr(self, name)
                # end if
            # end for

            self.__tearDownContext(result, context)
        except Exception:
            result.addError(self, self.__exc_info())
            ok = TYPE_ERROR
        # end try

        if ok == TYPE_SUCCESS:
            result.addSuccess(self)
        # end if
    # end def __runTearDown

    def addFixture(self, function, *args, **kwargs):
        """Add a function, with arguments, to be called just before the test.
        Functions added are called on a LIFO basis.

        fixture items are called only if setUp succeeds."""
        self._fixtures.append((function, args, kwargs))
    # end def addFixture

    def doFixtures(self):
        """Execute class Fixture functions. Normally called for you after
        tearDown."""
        outcome = self._outcome or _Outcome()
        while self._fixtures:
            function, args, kwargs = self._fixtures.pop()
            with outcome.testPartExecutor(self):
                function(*args, **kwargs)
            # end with
        # end while
    # end def doFixtures
# end class TestCase


class TestSuite(Test, UnitTestSuite):
    """
    A test suite is a composite test consisting of a number of TestCases.

    For use, create an instance of TestSuite, then add test case instances.

    When all tests have been added, the suite can be passed to a test
    runner. It will run the individual test cases
    in the order in which they were added, aggregating the results.

    When subclassing, do not forget to call the base class constructor.
    """
    def __init__(self, tests=tuple(), name=None):
        """
        :param tests: A map testCaseClass->List of test case names to add to this suite.
        :type tests: ``tuple|list``
        :param name: A name for this test suite.
        :type name: ``type|str|None``
        """
        Test.__init__(self)
        UnitTestSuite.__init__(self, tests)

        if isinstance(name, str):
            self.name = name
        elif name is not None:
            self.name = ".".join((str(name.__module__), str(name.__name__),))
        else:
            self.name = name
        # end if
    # end def __init__

    def __str__(self):
        """
        Obtain a friendly string representation of this object

        :return: The current object, as a string
        :rtype: ``str``
        """
        return "%s" % self.name
    # end def __str__

    def __repr__(self):
        """
        Obtain a string representation of this object.

        :return: String representation of this object
        :rtype: ``str``
        """
        return "<%s.%s tests=%s>" % (self.__class__.__module__,
                                     self.__class__.__name__,
                                     self._tests)
    # end def __repr__

    def id(self):
        """
        NB: This test id is only based on the class and method names.
        """
        return "%s" % (self.name or ("%s.%s" % (self.__class__.__module__, self.__class__.__name__)))
    # end def id

    # noinspection PyPep8Naming
    def shortDescription(self):
        """
        Return a one-line description of the test, or None if no description
        has been provided.

        :return: A short description of the test suite
        :rtype: ``str``
        """
        return self.__doc__.strip().split('\n', 1)[0]
    # end def shortDescription

    # noinspection PyPep8Naming
    def fullDescription(self):
        """
        Obtain  the full description (i.e. the docstring) of the test.

        :return: Description
        :rtype: ``str``
        """
        return self.__doc__
    # end def fullDescription

    def countTestCases(self):
        """
        Count the tests cases in the current suite, and in child suites if present.

        :return: Cases number
        :rtype: ``int``
        """
        cases = 0
        for test in self._tests:
            cases += test.countTestCases()
        # end for
        return cases
    # end def countTestCases

    def addTest(self, test):
        """
        Add a test to this test suite.

        :param test: The test to add to this suite.
        :type test: ``TestCase``
        """
        self._tests.append(test)
    # end def addTest

    def addTests(self, tests):
        """
        Add a collection of tests to the current suite.

        :param tests: The tests to add.
        :type tests: ``tuple[TestCase]``
        """
        for test in tests:
            self.addTest(test)
        # end for
    # end def addTests

    def __call__(self, result=None, context=None):
        """
        Run the test suite

        :param result: The test result used to collect test runs.
        :type result: ``TestResult``
        :param context: The context in which to call the tests.
        :type context: ``Context``
        """
        self.run(result, context)
    # end def __call__

    def run(self, result=None, context=None):
        """
        Run all tests from this suite.

        This method:
        - Filter the test depending on the context-provided filter.
          It is therefore possible to filter test based, for instance, on
          their name, their level, or any other predicate provided in the
          filter clause.
        - If the test matches the filter, it notifies the listeners that the test is about to start.
        - The test runs
        - The listeners are notified that the test has stopped.

        :param result: The test result used to collect test runs.
        :type result: ``TestResult``
        :param context: The context in which to call the tests.
        :type context: ``Context``
        """
        # Create inner instances of result and context, if none are found.
        # It is time-consuming, but allows PyHarness's tests to run within pyunit
        result = self._fixResult(result)
        context = self._fixContext(context)

        if self.canRunCore(result, context) and self.canRun(result, context):
            result.startTest(self)

            for test in self._tests:
                if isinstance(test, Test):
                    test.run(result, context)
                else:
                    test.run(result)
                # end if
            # end for

            result.stopTest(self)
        # end if
    # end def run

    # noinspection PyPep8Naming
    @staticmethod
    def _parseRunTestArgs(testModule, testClass, testName):
        """
        Parse arguments of tests.

        This utility method interprets the parameters depending on their type.
        This permits the runTest method to support various signatures.

        The output is a tuple containing:
        - The test parent
        - The test class
        - The test name

        :param testModule: Module of the test
        :type testModule: ``type``
        :param testClass: Class of the test
        :type testClass: ``type``
        :param testName: Name of the test
        :type testName: ``str``

        :return: Parsing result: A tuple (parent, class, name)
        :rtype: ``tuple[type|str|None, str, str]``
        """
        result = None

        # First, extract the test class from the arguments
        # This is case 1 an 2: Only one argument
        if testClass is None and testName is None:

            if isinstance(testModule, str):
                # Import the fqn, which should be a class
                testModule = importFqn(testModule)
            # end if

            if isinstance(testModule, type):
                # The first argument points to a class
                result = (None, testModule, testName)
            # end if

        elif testModule is not None and testClass is not None:
            # This is case 3, 4, 5: Two arguments
            if isinstance(testModule, str) and isinstance(testClass, str):

                # The first argument is either a class or a module.
                module = importFqn(testModule)
                parent = module
                child = getattr(module, testClass)

                if isinstance(parent, ModuleType) and isinstance(child, type):
                    result = (parent, child, testName)
                elif isinstance(parent, type):
                    # The second arguments contains the test name
                    result = (None, parent, testClass)
                # end if
            elif isinstance(testModule, type):
                # The first argument is a class, and the second is the test name
                result = (None, testModule, testClass)
            # end if
        # end if

        if result is None:
            raise ValueError(f"Unrecognized parameters: {str(testModule)}, {str(testClass)}, {str(testName)}")
        # end if

        return result
    # end def _parseRunTestArgs

    # noinspection PyPep8Naming
    def runTest(self, result, context, testModule, testClass=None, testName=None, aggregateToPyHarness=True):
        """
        Run a single test

        The arguments of this method can be:
         -# runTest(result, context, <class>)
         -# runTest(result, context, <classname>)
         -# runTest(result, context, <class>,       <testname>)
         -# runTest(result, context, <classname>,   <testname>)
         -# runTest(result, context, <packagename>, <classname>)
         -# runTest(result, context, <packagename>, <classname>, <testname>)

        :param result: The TestResult collector
        :type result: ``TestResult``
        :param context: Context of the test
        :type context: ``Context``
        :param testModule: Module of the test
        :type testModule: ``type``
        :param testClass: Class of the test - OPTIONAL
        :type testClass: ``type``
        :param testName: Name of the test - OPTIONAL
        :type testName: ``str``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        @todo If the first argument is a package, enumerate all tests in this package
        """
        context = self._fixContext(context)
        result = self._fixResult(result)

        # Extract information on the test from the parameters.
        testModule, testClass, testName = self._parseRunTestArgs(testModule, testClass, testName)

        # Can the test run ? By default, yes.
        can_run = True
        if issubclass(testClass, TestSuite):
            # The test is a pyharness.core.TestSuite
            # Create a new instance of the test, using the adaptor pattern
            test = testClass([], testName)
            can_run = test.canRun(result, context)

        elif issubclass(testClass, UnitTestSuite):
            # The test is an unittest.TestSuite
            # Create a new instance of the test, using the adaptor pattern
            # But first create a decorator
            if aggregateToPyHarness:
                testClass = TestLoader.makeAggregatingClass(TestSuite, testClass)
            # end if
            # noinspection PyArgumentList
            test = testClass([], testName)
            # noinspection PyUnresolvedReferences
            can_run = test.canRun(result, context)

        elif issubclass(testClass, TestCase) or issubclass(testClass, UnitTestCase):
            # The test is a test case (either a pyunit or a pyharness one)
            if testName is None:
                # The test is not designated by its name
                # Discover the list of test names from the test class, and
                # create a test suite that holds the child tests
                test = DEFAULT_TESTLOADER.loadTestsFromTestCase(testClass, aggregateToPyHarness=aggregateToPyHarness)
            else:
                # The test is designated by name: Create a test instance using the adaptor pattern
                if issubclass(testClass, UnitTestCase) and not issubclass(testClass, TestCase) and aggregateToPyHarness:
                    testClass = TestLoader.makeAggregatingClass(TestCase, testClass)
                # end if
                test = testClass(testName)

                # This designates ONE test: apply the filters to discover if
                # the test is allowed to run.
                # noinspection PyUnresolvedReferences
                can_run = context.filter(test) and test.canRun(result, context)
            # end if

        else:
            raise ValueError(f"Invalid test class: {str(testClass)}")
        # end if

        if can_run:
            test.run(result, context)
        # end if
    # end def runTest

    # noinspection PyMethodOverriding
    def debug(self, context):
        """
        Run the tests without collecting errors in a TestResult

        :param context: The context in which the test suite is run.
        :type context: ``Context``
        """
        for test in self._tests:
            # noinspection PyArgumentList
            test.debug(context)
        # end for
    # end def debug
# end class TestSuite


##############################################################################
# Locating and loading tests
##############################################################################
class TestLoader(object):
    """
    This class is responsible for loading tests according to various
    testcases and returning them wrapped in a Test
    """
    # The test function method prefix
    testMethodPrefix = 'test'

    testExcludedMethods = ('testCaseChecked', 'testCaseManualChecked')

    # The subTest function method prefix
    subTestMethodPrefix = 'subTest'

    @staticmethod
    def cmp(a, b):
        """If you really need the cmp() functionality,
        you could use the expression (a > b) - (a < b)"""
        return (a > b) - (a < b)
    # end def cmp

    # The default test method comparison function
    sortTestMethodsUsing = cmp

    # The default test suite class
    suiteClass = TestSuite

    # noinspection PyPep8Naming
    @staticmethod
    def makeAggregatingClass(myClass, parentClass):
        """
        Create an aggregation class, the adds pyharness.core.TestCase behaviour to unittest.TestCase classes

        :param myClass: The first parent class (from ``pyharness.core``)
        :type myClass: ``type|Test``
        :param parentClass: The parent class to decorate (from unittest)
        :type parentClass: ``type|Test``

        :return: A new aggregated class
        :rtype: ``AggregatingClass``
        """
        class AggregatingClass(myClass, parentClass):
            """
            A class aggregating the behaviour of TestCase and testCaseClass.
            """
            def __init__(self, *options, **kwargs):
                """
                :param options: Positional arguments
                :type options: ``tuple|str``
                :param kwargs: Keyword arguments
                :type kwargs: ``dict``
                """
                myClass.__init__(self, *options, **kwargs)
                parentClass.__init__(self, *options, **kwargs)
            # end def __init__

            def id(self):
                """
                Obtain  a (unique) test id.

                This test id is only based on the class and method names.

                :return: A test id
                :rtype: ``str``
                """
                return f"{parentClass.__module__}.{parentClass.__name__}.{self._testMethodName}"
            # end def id

            def __str__(self):
                """
                Obtain  the string representation of the current object.

                This redirects the method to the target instance

                :return: The current object, as a string
                :rtype: ``str``
                """
                return f"{self._testMethodName} ({parentClass.__module__}.{parentClass.__name__})"
            # end def __str__

            # noinspection PyPep8Naming
            def canRun(self, result, context):
                """
                @copydoc pyharness.core.Test.canRun
                """
                # noinspection PyArgumentList
                result = myClass.canRun(self, result, context)
                if hasattr(parentClass, 'canRun'):
                    # noinspection PyArgumentList
                    result = result and parentClass.canRun(self, result, context)
                # end if

                return result
            # end def canRun

            # noinspection PyPep8Naming
            def setUp(self, *options, **kwargs):
                """
                Test setup.

                :param options: Positional arguments
                :type options: ``tuple``
                :param kwargs: Keyword arguments
                :type kwargs: ``dict``
                """
                # noinspection PyUnresolvedReferences
                myClass.setUp(self, *options, **kwargs)
                # noinspection PyUnresolvedReferences
                parentClass.setUp(self, *options, **kwargs)
            # end def setUp

            # noinspection PyPep8Naming
            def tearDown(self, *options, **kwargs):
                """
                Test tearDown

                :param options: Positional arguments
                :type options: ``tuple``
                :param kwargs: Keyword arguments
                :type kwargs: ``dict``
                """
                # noinspection PyUnresolvedReferences
                parentClass.tearDown(self, *options, **kwargs)
                # noinspection PyUnresolvedReferences
                myClass.tearDown(self, *options, **kwargs)
            # end def tearDown
        # end class AggregatingClass

        AggregatingClass.__name__ = parentClass.__name__
        AggregatingClass.__module__ = parentClass.__module__

        return AggregatingClass
    # end def makeAggregatingClass

    # noinspection PyPep8Naming
    @classmethod
    def loadTestsFromTestCase(cls, testCaseClass, methodPredicate=lambda m: True, aggregateToPyHarness=True):
        """
        Return a suite of all tests cases contained in testCaseClass

        :param testCaseClass: The test case class that contains the tests.
        :type testCaseClass: ``type``
        :param methodPredicate: Predicate that returns True if the test method is acceptable - OPTIONAL
        :type methodPredicate: ``function``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        :return: A TestSuite, that contains the wrapped tests.
        :rtype: ``TestSuite``
        """
        # If the TestCase class is an instance of unittest.TestCase, we need to
        # make it behave as a pyharness.core.TestCase.
        # This is done by using multiple inheritance, where pyharness.core.TestCase
        # is the FIRST parent class.

        parent_class = testCaseClass

        if (issubclass(testCaseClass, UnitTestCase) and (not issubclass(testCaseClass, TestCase))
                and aggregateToPyHarness):
            parent_class = testCaseClass
            testCaseClass = cls.makeAggregatingClass(TestCase, parent_class)
        # end if

        test_cases = [testCaseClass(name) for name in cls.getTestCaseNames(testCaseClass,
                                                                           methodPredicate=methodPredicate)]
        return cls.suiteClass(test_cases, parent_class)
    # end def loadTestsFromTestCase

    # noinspection PyPep8Naming
    @classmethod
    def loadTestsFromModule(cls, module, classPredicate=lambda c: True, methodPredicate=lambda m: True,
                            aggregateToPyHarness=True):
        """
        Return a suite of all tests cases contained in the given module

        This method uses python's introspection mechanisms to discover the tests
        present in a module.

        :param module: The module that contains the test cases
        :type module: ``ModuleType``
        :param classPredicate: A predicates that accepts or rejects the class type - OPTIONAL
        :type classPredicate: ``Callable``
        :param methodPredicate: A predicates that accepts or rejects the method type - OPTIONAL
        :type methodPredicate: ``function``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        :return: A TestSuite containing the tests contained in the given module
        :rtype: ``TestSuite``
        """
        tests = []

        # Iterate on all children of a module.
        for name in dir(module):
            obj = getattr(module, name)

            # Only load the tests declared in the current module
            if (isinstance(obj, type) and (issubclass(obj, TestCase) or issubclass(obj, UnitTestCase))
                    and (classPredicate(obj)) and (obj.__module__ == module.__name__)):
                # If the current child is a TestCase, load tests from the test case
                tests.append(cls.loadTestsFromTestCase(obj, methodPredicate, aggregateToPyHarness=aggregateToPyHarness))

            elif (isinstance(obj, type) and (issubclass(obj, TestSuite) or issubclass(obj, UnitTestSuite))
                  and classPredicate(obj) and obj.__module__ == module.__name__):
                # If the current child is a TestSuite, create a new instance of the suite.
                tests.append(obj())
            # end if
        # end for

        # The tests will actually be put under the package name
        # Create an intermediate suite, that holds the discovered tests.
        return cls.suiteClass(tests, module.__name__)
    # end def loadTestsFromModule

    # noinspection PyPep8Naming
    def loadTestsFromName(self, name, module=None, aggregateToPyHarness=True):
        """
        Return a suite of all tests cases given a string specifier.

        :param name: The string specifier used to obtain the tests.
        :type name: ``str``
        :param module: The root module used to search test cases.
        :type module: ``type|None``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        :return: A test suite containing all the tests extracted from the specifier
        :rtype: ``TestSuite``

        The name may resolve either to a module, a test case class, a
        test method within a test case class, or a callable object which
        returns a TestCase or TestSuite instance.

        The method optionally resolves the names relative to a given module.
        """
        test_class = None
        parts = name.split('.')
        if module is None:
            if not parts:
                raise ValueError("incomplete test name: %s" % (name,))
            else:
                parts_copy = parts[:]
                while parts_copy:
                    try:
                        # This cannot be replaced by importFqn
                        # (Implements a fallback mechanism on deepest module)
                        module = __import__('.'.join(parts_copy))  # Do not replace __import__ by importFqn !
                        break
                    except ImportError:
                        # The import error is not logged, because it _can_ happen
                        # when importing test classes and methods
                        del parts_copy[-1]
                        if not parts_copy:
                            raise
                        # end if
                    # end try
                # end while
                parts = parts[1:]
            # end if
        # end if

        obj = module
        for part in parts:
            test_class = obj
            obj = getattr(obj, part)
        # end for

        if isinstance(obj, ModuleType):
            # The object is a module.
            # Extract all tests from the module
            return self.loadTestsFromModule(obj, aggregateToPyHarness=aggregateToPyHarness)
        elif isinstance(obj, type) and (issubclass(obj, TestCase) or issubclass(obj, UnitTestCase)):
            # The object is a TestCase, lookup all its test method.
            return self.loadTestsFromTestCase(obj, aggregateToPyHarness=aggregateToPyHarness)
        elif isinstance(obj, FunctionType):
            # testClass = obj.__class__
            if issubclass(test_class, UnitTestCase) and (not issubclass(test_class, TestCase)):
                test_class = self.makeAggregatingClass(TestCase, test_class)
            # end if
            # noinspection PyCallingNonCallable
            return test_class(obj.__name__)
        elif hasattr(obj, '__call__'):
            # noinspection PyCallingNonCallable
            test = obj()

            if not isinstance(test, TestCase) and not isinstance(test, TestSuite):
                raise ValueError(f"calling {obj} returned {test}, not a test")
            # end if
            return test
        elif isinstance(obj, type):
            # noinspection PyUnresolvedReferences
            test_class = obj.__self__.__class__
            if issubclass(test_class, UnitTestCase) and not issubclass(test_class, TestCase) and aggregateToPyHarness:
                test_class = self.makeAggregatingClass(TestCase, test_class)
            # end if
            return test_class(obj.__name__)
        else:
            raise ValueError(f"don't know how to make test from: {obj}")
        # end if
    # end def loadTestsFromName

    # noinspection PyPep8Naming
    def loadTestsFromNames(self, names, module=None, aggregateToPyHarness=True):
        """
        Return a suite of all tests cases found using the given sequence
        of string specifiers.

        :param names: A sequence of string specifiers
        :type names: ``tuple[str]``
        :param module: The root module used to search test cases.
        :type module: ``type|None``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        :return: TestSuite containing the tests matching the given names
        :rtype: ``TestSuite``
        """
        if len(names) == 1:
            return self.loadTestsFromName(names[0], module, aggregateToPyHarness=aggregateToPyHarness)
        # end if

        suites = []
        for name in names:
            suites.append(self.loadTestsFromName(name, module, aggregateToPyHarness=aggregateToPyHarness))
        # end for

        return self.suiteClass(suites)
    # end def loadTestsFromNames

    # noinspection PyPep8Naming
    @classmethod
    def findTestsInSrcPath(cls, path, rootFQN="", classPredicate=lambda c: True, methodPredicate=lambda m: True,
                           useTestRunner=True, rootTestRunner=False, zipContext=None, aggregateToPyHarness=True):
        """
        Return a suite of all tests cases under the given path.

        The path should be in the PYTHONPATH

        :param path: The path in which to look for tests
        :type path: ``str``
        :param rootFQN: The root Fully Qualified Name of the module in the given path - OPTIONAL
        :type rootFQN: ``str``
        :param classPredicate: A predicates that accepts or rejects the class type - OPTIONAL
        :type classPredicate: ``function``
        :param methodPredicate: A predicates that accepts or rejects the method type - OPTIONAL
        :type methodPredicate: ``function``
        :param useTestRunner: Flag indicating whether to rely on suites found in testrunner.py files, or to find all
                              tests - OPTIONAL
        :type useTestRunner: ``bool``
        :param rootTestRunner: Flag indicating whether the API is called by a testrunner - OPTIONAL
                               This is needed for automated discovery.
        :type rootTestRunner: ``bool``
        :param zipContext: Context when looking for source files in .egg - OPTIONAL
        :type zipContext: ``dict``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        :return: A sequence of tests
        :rtype: ``list[TestCase]``
        """
        zip_clear = False
        if zipContext is None:
            zip_clear = True
            zipContext = {}
        # end if

        tests = []

        matched = []

        # Process python scripts
        dir_contents = listdir(path)
        pyfiles = sorted(set([se[0] for se in [splitext(f) for f in dir_contents] if (se[-1] in _SUFFIXES)]))

        # If a testrunnner.py is found, only consider the test runner, and not other scripts or sub-packages
        if useTestRunner and not rootTestRunner and 'testrunner' in pyfiles:
            pyfiles = ['testrunner']
        else:
            # Process python subdirectories
            pydirs = [f for f in dir_contents if isdir(join(path, f))]
            for pydir in pydirs:

                # If the module is a directory, do a recursive load
                childPath = join(path, pydir)

                if not exists(join(childPath, '__init__.py')):
                    # Repositories which are not python packages are excluded
                    continue
                # end if

                # Attempt to import the package
                package = importFqn((rootFQN + pydir).strip('.'), False)
                if package is not None:
                    sub_tests = cls.findTestsInSrcPath(childPath, rootFQN + pydir + ".", classPredicate=classPredicate,
                                                       methodPredicate=methodPredicate, useTestRunner=useTestRunner,
                                                       zipContext=zipContext, aggregateToPyHarness=aggregateToPyHarness)
                    tests.extend(sub_tests)
                # end if
            # end for
        # end if

        # Process python scripts
        for name in pyfiles:

            # The module fully qualified name
            fqn = (rootFQN + name).strip('.')
            if fqn not in matched:

                matched.append(fqn)

                # Import the module, and its reference
                module = importFqn(fqn, False)

                if module is not None:
                    # append all tests in this module
                    sub_tests = cls.loadTestsFromModule(module, classPredicate=classPredicate,
                                                        methodPredicate=methodPredicate,
                                                        aggregateToPyHarness=aggregateToPyHarness)
                    if sub_tests.countTestCases() > 0:
                        tests.append(sub_tests)
                    # end if
                # end if
            # end if
        # end for

        if zip_clear:
            for zipFile in list(zipContext.values()):
                zipFile.close()
            # end for
        # end if

        return tests
    # end def findTestsInSrcPath

    # noinspection PyPep8Naming
    @classmethod
    def findTestsInSrcPaths(cls, paths, classPredicate=lambda c: True, methodPredicate=lambda m: True,
                            aggregateToPyHarness=True):
        """
        Return a suite of all tests cases found using the given sequence
        of paths.

        :param paths: A sequence of paths.
        :type paths: ``tuple[str]``
        :param classPredicate: A predicates that accepts or rejects the class type - OPTIONAL
        :type classPredicate: ``callable``
        :param methodPredicate: A predicates that accepts or rejects the method type - OPTIONAL
        :type methodPredicate: ``function``
        :param aggregateToPyHarness: Flag indicating whether the test should be aggregated to PyHarness - OPTIONAL
        :type aggregateToPyHarness: ``bool``

        :return: A sequence of TestSuite instances, found in the TESTSUITES path
        :rtype: ``list[TestSuite]``
        """
        suites = []
        for path in paths:
            suites.extend(cls.findTestsInSrcPath(path, classPredicate=classPredicate, methodPredicate=methodPredicate,
                                                 aggregateToPyHarness=aggregateToPyHarness))
        # end for
        return suites
    # end def findTestsInSrcPaths

    # noinspection PyPep8Naming
    @classmethod
    def getTestCaseNames(cls, testCaseClass, methodPredicate=lambda m: True):
        """
        Return a sorted sequence of method names found within testCaseClass

        This method also searches for tests implemented in the class hierarchy

        :param testCaseClass: The class containing the test methods.
        :type testCaseClass: ``type``
        :param methodPredicate: Predicate that accepts a test case method - OPTIONAL
        :type methodPredicate: ``function``

        :return: A sequence of methods that match the method prefix
        :rtype: ``list[str]``
        """
        test_fn_names = [fnName for fnName in dir(testCaseClass) if (
            (fnName.startswith(cls.testMethodPrefix) and (fnName not in cls.testExcludedMethods)))]

        sub_test_fn_names = [fnName for fnName in dir(testCaseClass) if fnName.startswith(cls.subTestMethodPrefix)]

        for baseclass in testCaseClass.__bases__:
            for testFnName in cls.getTestCaseNames(baseclass):
                # Handle overridden methods
                if testFnName not in test_fn_names:
                    test_fn_names.append(testFnName)
                # end if
            # end for
        # end for

        if (len(sub_test_fn_names) > 0 and ('subTestRunner' not in test_fn_names) and
                ('subTestRunner' in dir(testCaseClass))):
            test_fn_names.append('subTestRunner')
        # end if

        filtered_test_fn_names = []

        # Filter out the methods based on the methodPredicate
        for testFnName in test_fn_names:
            # Handle decorators and proxies
            obj = getattr(testCaseClass, testFnName)
            while hasattr(obj, "next"):
                obj = obj.__next__
            # end while

            if methodPredicate(obj):
                filtered_test_fn_names.append(testFnName)
            # end if
        # end for

        test_fn_names = filtered_test_fn_names

        if cls.sortTestMethodsUsing:
            test_fn_names.sort(key=TestRunner.cmp_to_key(cls.sortTestMethodsUsing))
        # end if

        return test_fn_names
    # end def getTestCaseNames
# end class TestLoader


DEFAULT_TESTLOADER = TestLoader()


class TestRunner(object):
    """
    A test runner that attaches listeners to new instances of a TestResult.

    A listener is an instance of a TestListener-derived class, that
    implements callback methods. Those methods will be called during the test
    execution, to notify the listener of various events.
    """
    def __init__(self, listeners=None, *unused):
        """
        :param listeners: The listeners that will receive test progress notifications
        :type listeners: ``list[Listener]``
        :param unused: Additional options, not used by the base implementation
        :type unused: ``tuple``
        """
        self.listeners = listeners or ()
    # end def __init__

    # noinspection PyPep8Naming
    def _attachListeners(self, result):
        """
        This protected method attaches the listeners to the current runner.

        This permits each listener to be notified of the events it is interesed
        in, and only of those events. It also provides an efficient way to prevent
        cuttering the execution with unused notifications.

        See the HOWTO in the reference manual for a tutorial on writing TestListeners.

        :param result: The result the listeners will be attached to.
        :type result: ``TestResult``
        """
        for listener in self.listeners:
            listener.attach(result)
        # end for
    # end def _attachListeners

    # noinspection PyPep8Naming
    def _detachListeners(self, result):
        """
        This protected method detaches the listeners from the current runner.

        This is a cleanup method, that should be called in order to reduce the
        number of objects kept in-memory.

        :param result: The result the listeners should be detached from.
        :type result: ``TestResult``
        """
        for listener in self.listeners:
            listener.detach(result)
        # end for
    # end def _detachListeners

    def run(self, tests, context=None):
        """
        Run the given test case or test suite, or sequence of test cases or test suites.

        This method:
        - attaches the listeners provided in the constructor
        - Runs the test
        - Detaches listeners
        .

        :param tests: The test case or test suite to run
        :type tests: ``Test|tuple[Test]``
        :param context: The context in which to call the tests - OPTIONAL
        :type context: ``Context|None``

        :return: Result of the run
        :rtype: ``TestResult``
        """
        raise NotImplementedError()
    # end def run

    def pause(self, forcefully=False):
        """
        Pause the execution, if possible

        :param forcefully: Flag indicating whether the current test must be paused.
        :type forcefully: ``bool``
        """
        raise NotImplementedError()
    # end def pause

    def stop(self, forcefully=False):
        """
        Stop the execution, if possible

        :param forcefully: Flag indicating whether the current test must be aborted.
        :type forcefully: ``bool``
        """
        raise NotImplementedError()
    # end def stop

    def resume(self):
        """
        Resume a paused execution, if possible.
        """
        raise NotImplementedError()
    # end def resume

    @staticmethod
    def cmp_to_key(mycmp):
        """Convert a cmp= function into a key= function"""
        class K(object):
            # noinspection PyUnusedLocal
            def __init__(self, obj, *args):
                self.obj = obj
            # end def __init__

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0
            # end def __lt__

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0
            # end def __gt__

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0
            # end def __eq__

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0
            # end def __le__

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0
            # end def __ge__

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0
            # end def __ne__
        # end class K
        return K
    # end def cmp_to_key
# end class TestRunner


class MonoThreadTestRunner(TestRunner):
    """
    A Mono-threaded instance of a TestRunner.

    It attaches listeners to new instances of a TestResult.

    A listener is an instance of a TestListener-derived class, that
    implements callback methods. Those methods will be called during the test
    execution, to notify the listener of various events.
    """
    def __init__(self, listeners=None, *options):
        """
        :param listeners: The listeners that will received test progress notifications
        :type listeners: ``tuple[Listener]|list[Listener]``
        :param options: Additional options, not used
        :type options: ``tuple``
        """
        TestRunner.__init__(self, listeners, *options)

        self._stop = False
        self._lock = RLock()
        self._context = None
    # end def __init__

    def run(self, tests, context=None):
        # See ``pyharness.core.TestRunner.run``
        result = TestResult()

        self._attachListeners(result)

        if isinstance(tests, TestCase) or isinstance(tests, TestSuite):
            tests = (tests,)
        # end if

        try:
            self._context = context
            result.startRun(context, False)
            for test in tests:
                try:
                    if not (self._lock.acquire(False)):
                        result.stopRun(True)
                        self._lock.acquire(False)
                        result.startRun(context, True)
                    # end if
                finally:
                    self._lock.release()
                # end try

                if not self._stop:
                    test.run(result, self._context)
                # end if
            # end for

        finally:
            result.stopRun(False)
            self._detachListeners(result)
            self._context = None
        # end try

        return result
    # end def run

    def pause(self, forcefully=False):
        """
        @copydoc pyharness.core.TestRunner.pause
        """
        self._lock.acquire()
        if self._context is not None:
            self._context.abort = forcefully
        # end if
    # end def pause

    def stop(self, forcefully=False):
        """
        @copydoc pyharness.core.TestRunner.stop
        """
        self._stop = True
        if self._context is not None:
            self._context.abort = forcefully
        # end if
        self.resume()
    # end def stop

    def resume(self):
        """
        Resumes the execution, if possible
        """
        self._lock.release()
    # end def resume
# end class MonoThreadTestRunner


class MultiThreadTestRunner(TestRunner):
    """
    A multithreaded implementation of a TestRunner.

    The difference with the TestRunner class is that the run argument has
    alternate parameters:
    - A sequence of tests
    - The context
    - A maximum number of threads to use
    .
    """

    class RunTestTask(Task):
        """
        A simple task
        """

        # noinspection PyPep8Naming
        def __init__(self, targetTest, result, context):
            """
            Task constructor: keep the target test as a member variable

            :param targetTest: The test to run
            :type targetTest: ``TestCase``
            :param result: The results collector
            :type result: ``TestResult``
            :param context: The context to run the test in
            :type context: ``Context``
            """
            # noinspection PyTypeChecker
            Task.__init__(self, self._runTest, targetTest, result, context)
        # end def __init__

        # noinspection PyPep8Naming
        @staticmethod
        def _runTest(targetTest, result, context):
            """
            Run the test

            :param targetTest: The test to run
            :type targetTest: ``TestCase``
            :param result: The results collector
            :type result: ``TestResult``
            :param context: The context to run the test in
            :type context: ``Context``
            """
            # noinspection PyBroadException
            try:
                targetTest.run(result, context)
            except Exception:
                # This is used to debug internal exceptions in the run
                # (usually a flaky TestListener)
                raise
            # end try
        # end def _runTest

        def __str__(self):
            """
            Obtain a string representation of the task.

            :return: (str) The current task, as a string describing the test being run.
            """
            return str(self.args[0])
        # end def __str__
    # end class RunTestTask

    # noinspection PyPep8Naming
    def __init__(self, listeners=None, nThreads=5):
        """
        :param listeners: The listeners that will received test progress notifications
        :type listeners: ``tuple[Listener]|list[Listener]``
        :param nThreads: The number of threads that run concurrently - OPTIONAL
        :type nThreads: ``int``
        """
        TestRunner.__init__(self, listeners)
        self.nThreads = nThreads
        self._maxThreadLock = Semaphore(self.nThreads)
        self._executor = None
        self._context = None
    # end def __init__

    def pre_execute_thread(self):
        """
        Pre execute callback
        """
        pass
    # end def pre_execute_thread

    @staticmethod
    def post_execute_thread():
        """
        Post execute callback
        """
        pass
    # end def post_execute_thread

    # noinspection PyPep8Naming
    @staticmethod
    def __filterSubTests(tests):
        """
        Filter out subTests from the collection
        This is needed so that subTests are not run separately
        from their parent

        :param tests: The tests to filter out.
        :type tests: ``list[TestCase,TestSuite]``

        :return: The list of acceptable tests
        :rtype: ``list[TestCase]``
        """

        # noinspection PyPep8Naming
        def _filterSubTests(test):
            """
            Filter out subTests from the collection
            This is needed so that subTests are not run separately
            from their parent

            :param test: The test to filter out.
            :type test: ``Test``

            :return: Flag indicating whether the test is acceptable (True) or not (False)
            :rtype: ``bool``
            """
            if isinstance(test, TestCase):
                # noinspection PyProtectedMember
                testMethodName = test._testMethodName
                if testMethodName != 'subTestRunner' and testMethodName.startswith(TestLoader.subTestMethodPrefix):
                    return False
                # end if
            # end if
            return True
        # end def _filterSubTests

        return [test for test in tests if _filterSubTests(test)]
    # end def __filterSubTests

    # noinspection PyPep8Naming
    def __collectTests(self, tests, context):
        """
        Collects the tests to be run.

        :param tests: The initial list of tests
        :type tests: ``tuple[Test]``
        :param context: The context the tests are to be run in
        :type context: ``Context``

        :return: A list of tests to run.
        rtype: ``list[TestCase,TestSuite]``
        """
        # Contrary to the MonoThreadTestRunner, tests are collected first,
        # and run second.
        class CollectContext(object):
            """
            A context that only collects test data
            """
            # noinspection PyShadowingBuiltins
            def __init__(self, next):
                """
                :param next: The decorated context.
                :type next: ``Context``
                """
                self.next = next
            # end def __init__

            def __getattr__(self, name):
                """
                Obtain the attribute of the decorated instance

                :param name: The attribute name
                :type name: ``str``

                :return: The attribute value
                :rtype: ``str``
                """
                return getattr(self.__dict__["next"], name)
            # end def __getattr__

            # noinspection PyPep8Naming
            # noinspection PyMethodMayBeStatic
            def collectOnly(self):
                """
                Whether to collect data (True) or to run the test (False)

                :return: True
                :rtype: ``bool``
                """
                return True
            # end def collectOnly
        # end class CollectContext

        # IMPORTANT: The collected test must preserve the order in which the
        #            tests have been discovered. Using a set here will result in
        #            a random order of execution
        collectedTests = []

        class CollectListener(TestListener):
            """
            @copydoc pyharness.core.TestListener
            """

            def __init__(self):
                TestListener.__init__(self, None, None, None, None)
                self.ignoreCollection = False
            # end def __init__

            def startTest(self, test):
                """
                @copydoc pyharness.core.TestListener.startTest
                """
                if isinstance(test, TestCase):
                    collectedTests.append(test)
                # end if
            # end def startTest
        # end class CollectListener

        collectListeners = [listener for listener in self.listeners if (not listener.ignoreCollection)]

        collectContext = CollectContext(context)
        collectListeners.append(CollectListener())
        collectTestRunner = MonoThreadTestRunner(collectListeners)

        # Multiply the tests by the loop count
        tests = tests * context.getLoopCount()

        suite = TestSuite(tests)
        collectTestRunner.run(suite, collectContext)

        return collectedTests
    # end def __collectTests

    def run(self, tests, context=None):
        # See ``pyharness.core.TestRunner.run``
        context.abort = False

        if isinstance(tests, TestCase) or isinstance(tests, TestSuite):
            tests = (tests,)
        # end if

        result = TestResult()
        self._attachListeners(result)
        result.startRun(context, False)

        tests = self.__collectTests(tests, context)
        tests = self.__filterSubTests(tests)

        # Sort the tests in an order defined by a policy (i.e. fastest-first,
        # slowest-first, alphabetical order, lowest-level first...)
        tests.sort(key=self.cmp_to_key(context.sorter))

        # Start by creating an executor, with the required number of threads.
        tasks = []

        for test in tests:
            tasks.append(self.RunTestTask(test, result, context))
        # end for
        del tests

        # noinspection PyPep8Naming
        def onSuspend():
            """
            Notified when all threads are suspended
            """
            result.stopRun(True)
        # end def onSuspend

        # noinspection PyPep8Naming
        def onResume():
            """
            Notified when all threads are resumed
            """
            result.startRun(context, True)
        # end def onResume

        self._executor = ThreadedExecutor(tasks, max_threads=self.nThreads, name="TestRunner", on_suspend=onSuspend,
                                          on_resume=onResume, pre_execute_thread=self.pre_execute_thread,
                                          post_execute_thread=self.post_execute_thread)
        try:
            self._context = context
            self._executor.execute()

        finally:
            result.stopRun(False)
            self._detachListeners(result)
            self._context = None
        # end try
    # end def run

    def pause(self, forcefully=False):
        # See ``pyharness.core.TestRunner.pause``
        executor = self._executor
        assert executor is not None

        executor.pause()
        if self._context is not None:
            self._context.abort = forcefully
        # end if
    # end def pause

    def stop(self, forcefully=False):
        # See ``pyharness.core.TestRunner.stop``
        executor = self._executor
        assert executor is not None

        executor.stop()
        if self._context is not None:
            self._context.abort = forcefully
        # end if
    # end def stop

    def resume(self):
        """
        @copydoc pyharness.core.TestRunner.resume
        """
        executor = self._executor
        assert executor is not None

        if self._context is not None:
            self._context.abort = False
        # end if
        executor.resume()
    # end def resume
# end class MultiThreadTestRunner


class MonoThread(object):
    """
    Function decorator, that marks a function definition as monothread-only.

    This should be used in tests, on test methods, to declare the test as monothread-only.
    By default, tests are not limited to one thread.

    Example:
    @code
    from pyharness.core import TestCase
    from pyharness.core import monothread
    class MyTest(TestCase):

        @monothread
        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example
    # end class MyTest
    @endcode
    """
    def __init__(self):
        self._idToThreadCount = {}
    # end def __init__

    def __call__(self, function):
        """
        monothread decorator call function

        :param function: The capture function
        :type function: ``callable``

        :return: The captured function
        :rtype: ``Function``

        NB: This function will be called when using a @c @@monothread(...) decorator.
        """
        self._idToThreadCount[id(function)] = 0

        return function
    # end def __call__

    # noinspection PyPep8Naming
    @staticmethod
    def __realFunction(f):
        """
        Extract the inner FunctionType object from a MethodType object.

        :param f: A MethodType object, from which the FunctionType object is extracted
        :type f: ``MethodType``

        :return: The FunctionType object associated with the parameter
        :rtype: ``Function``
        """
        func = f
        while isinstance(func, MethodType):
            func = func.__func__
        # end while
        return func
    # end def __realFunction

    # noinspection PyPep8Naming
    def getThreadLimit(self, f):
        """
        Obtain the thread limit for this function.

        :param f: The MethodType object to test
        :type f: ``method``

        :return: The thread limit for the function, None if not defined
        """
        func = self.__realFunction(f)
        f_id = id(func)
        return self._idToThreadCount.get(f_id, None)
    # end def getThreadLimit
# end class MonoThread


# The global monothread monitor. Its name should be ignored by pylint
monothread = MonoThread()

# This hack replaces unittest's defaultTestLoader by PyHarness's implementation.
# This is ugly, but allows IDEs like pydev to


__oldGetTestCaseNames = unittest.defaultTestLoader.getTestCaseNames


# noinspection PyPep8Naming
def __getTestCaseNames(testCaseClass):
    """
    Return a sorted sequence of method names found within testCaseClass

    :param testCaseClass: The test case class to filter
    :type testCaseClass: ``Type``

    :return: The filtered list
    :rtype: ``list[str]``
    """
    test_fn_names = __oldGetTestCaseNames(testCaseClass)
    return [testFnName for testFnName in test_fn_names if testFnName not in ('testCaseChecked',
                                                                             'testCaseManualChecked')]
# end def __getTestCaseNames


unittest.defaultTestLoader.getTestCaseNames = __getTestCaseNames


# This hack replaces unittest's default _TextTestResult by PyHarness's implementation.
# This is ugly, but produces a much nicer output for test suites.
# noinspection PyProtectedMember
# noinspection PyUnresolvedReferences
__oldStartTest = unittest._TextTestResult.startTest


# noinspection PyPep8Naming
def __startTest(self, test):
    """
    Start a test notification for unittest

    :param test: The test to start.
    :type test: ``Test``
    """
    if not isinstance(test, TestSuite):
        __oldStartTest(self, test)
    # end if
# end def __startTest


# noinspection PyProtectedMember
# noinspection PyUnresolvedReferences
unittest._TextTestResult.startTest = __startTest

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
