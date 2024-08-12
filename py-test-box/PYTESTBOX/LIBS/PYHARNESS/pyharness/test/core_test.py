#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pyharness.test.coretest
    :brief: Core test implementation
            This is the main pyharness test implementation, that tests the core module.
    :author: Christophe roquebert
    :date: 2018/09/11
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from shutil import rmtree
from threading import Lock
from threading import RLock
from threading import Thread
from time import sleep
from unittest import TestCase
from weakref import ref

from pyharness.arguments import KeywordArguments
from pyharness.core import MonoThreadTestRunner
from pyharness.core import MultiThreadTestRunner
from pyharness.core import TYPE_FAILURE
from pyharness.core import TestCase as CoreTestCase
from pyharness.core import TestException
from pyharness.core import TestResult
from pyharness.core import _ALL_LEVELS
from pyharness.core import _LEVEL_INFO
from pyharness.core import _LEVEL_RAW
from pyharness.core import monothread
from pyharness.systems import AbstractSubSystem
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MockContext(object):
    """
    A fake context, for the testlisteners.
    """
    abort = False
    kill = False
    collectOnly = lambda self: False

    @staticmethod                                                           # pylint:disable=W0613
    def filter(*args, **kwargs):                                            #@ReservedAssignment pylint:disable=W0613
        """
        Filters the test

        :param args: The arguments - OPTIONAL
        :type args: ``tuple``
        :param kwargs: The keyword arguments - OPTIONAL
        :type kwargs: ``tuple``

        :return: Always True
        :rtype: ``bool``
        """
        return True
    # end def filter

    @staticmethod                                                           # pylint:disable=W0613
    def sorter(*args, **kwargs):                                            # pylint:disable=W0613
        """
        Sorters for the test

        :param args: The arguments - OPTIONAL
        :type args: ``tuple``
        :param kwargs: The keyword arguments - OPTIONAL
        :type kwargs: ``tuple``

        :return: Always 0
        :rtype: ``int``
        """
        return 0
    # end def sorter

    @staticmethod
    def getCurrentMode():
        """
        Obtain a mock value

        :return: The mock value
        """
        return "MockMode"
    # end def getCurrentMode

    @staticmethod
    def getCurrentProduct():
        """
        Obtain a mock value

        :return: The mock value
        """
        return "MockProduct"
    # end def getCurrentProduct

    @staticmethod
    def getCurrentVariant():
        """
        Obtain a mock value

        :return: The mock value
        """
        return "MockVariant"
    # end def getCurrentVariant

    @staticmethod
    def getCurrentTarget():
        """
        Obtain a mock value

        :return: The mock value
        """
        return "MockTarget"
    # end def getCurrentTarget

    @staticmethod
    def getLoopCount():
        """
        Obtain a mock value

        :return: The mock value
        """
        return 1
    # end def getLoopCount

    @staticmethod
    def getFeatures():
        """
        Obtains mock features

        :return: mock features
        """
        root = AbstractSubSystem(None)
        runtime = AbstractSubSystem('RUNTIME')
        setattr(runtime, 'F_RandSeed', 0)
        setattr(root, 'RUNTIME', runtime)

        return root
    # end def getFeatures

    def getParent(self):
        """
        Obtains mock parent

        :return: mock parent
        """
        return self
    # end def getParent
# end class MockContext


def instantiate_mock_test(param_test_method_name, param_test_method_doc):
    """
    Creates a new Mock test case.

    This is defined as a function, so that the auto-discovery does not detect it
    as a test.

    :param param_test_method_name: The name of the test
    :type param_test_method_name: ``str``
    :param param_test_method_doc: The short description of the test
    :type param_test_method_doc: ``str``

    :return: A new instance of a MockTestCase
    """

    class InnerMockTest(TestCase):
        """
        A mock test case
        """

        def __init__(self, test_method_name, test_method_doc):
            """
            Constructor

            :param test_method_name: The name of the test
            :type test_method_name: ``str``
            :param test_method_doc: The short description of the test
            :type test_method_doc: ``str``
            """

            self._testMethodName = test_method_name
            self._testMethodDoc = test_method_doc
            self.warning_occurred = False

            super().__init__()
        # end def __init__
        
        def id(self):
            mock_id = super().id()
            return mock_id.replace('.MockTest.<locals>', '')
        # def id
    # end class InnerMockTest

    return InnerMockTest(param_test_method_name, param_test_method_doc)
# end def instantiate_mock_test


class TestResultTestCase(TestCase):
    """
    Tests the TestResult class
    """

    def test_StartStop(self):
        """Tests test count"""
        test_result = TestResult()

        self.assertEqual(0, test_result.testsRun, "Invalid initial test count")
        test_result.startTest(self)
        test_result.stopTest(self)
        self.assertEqual(1, test_result.testsRun, "Invalid final test count")
    # end def test_StartStop
# end class TestResultTestCase


class TestRunnerTestCase(TestCase):
    """
    Tests the TestRunner class

    A TestRunner only has the @c run method to test.
    """

    @staticmethod
    def isAbstract():
        """
        Used to detect whether the class is abtract, or contains an implementation.

        @return True if the class is abstract, False otherwise.
        """
        return True
    # end def isAbstract

    @staticmethod
    def _getTestRunnerClass():
        """
        Obtains a generator for the class under test
        """
        raise NotImplementedError
    # end def _getTestRunnerClass

    def test_RunMethod(self):
        """
        Tests the @c run method of the TestRunner class and its children.
        """

        if not self.isAbstract():
            test_runner_class = self._getTestRunnerClass()

            test_runner = test_runner_class()
            # Create 50 tests to run
            n_tests = 50
            tests = []
            for i in range(n_tests):
                class InnerTestCase(CoreTestCase):
                    """
                    Internal test, that always succeeds if i is even
                    """
                    def runTest(self):
                        """
                        The do-nothing test
                        """
                        self.assertEqual(0,
                                         i & 1,
                                         "Test voluntarily fails")
                    # end def runTest
                # end class InnerTestCase
                test = InnerTestCase()
                tests.append(test)
            # end for

            context = MockContext()

            # Run in a different thread
            inner_excp = [False]

            def worker():
                """
                A worker function, running the testrunner in a separate thread
                """
                try:
                    test_runner.run(tests, context)
                    inner_excp[0] = True
                except Exception as excp:                                                  # pylint:disable=W0703
                    inner_excp[0] = excp
                # end try
            # end def worker

            thread1 = Thread(target=worker, name="UserThread 1")
            thread1.start()

            quantum = 0.1
            while inner_excp[0] is False:
                sleep(quantum)
            # end while

            if inner_excp[0] is not True:
                raise ValueError('Inner exception should be true')
            # end if

        # end if
    # end def test_RunMethod

    def test_MonothreadDecorator(self):
        """
        Tests the monothread decorator
        """

        if not self.isAbstract():
            test_runner_class = self._getTestRunnerClass()

            test_runner = test_runner_class()
            # Create 50 tests to run
            n_tests = 50
            quantum = 0.1
            tests = []
            global_exc = [None]

            class InnerTestCase(TestCase):
                """
                Internal test, that always succeeds if i is even
                """

                __STATE = 0

                @monothread
                def test_Monothread_0(self):
                    """
                    A monothreaded test, that periodically checks the value of a counter
                    """
                    state = self.__STATE
                    sleep(n_tests * quantum)

                    try:
                        self.assertEqual(state,
                                         self.__STATE,
                                         "Multithreaded corruption.")
                    except Exception as excp:                                                # pylint:disable=W0703
                        global_exc[0] = excp
                    # end try
                # end def test_Monothread_0

                @classmethod
                def templateTest(cls):
                    """
                    A monothreaded test, that periodically checks the value of a counter
                    """
                    sleep(quantum)
                    cls.__STATE += 1
                # end def templateTest
            # end class InnerTestCase

            tests.append(InnerTestCase('test_Monothread_0'))
            for i in range(1, n_tests):
                test_name = "test_Monothread_%d" % i
                setattr(InnerTestCase, test_name, InnerTestCase.templateTest)
                tests.append(InnerTestCase(test_name))
            # end for

            context = MockContext()

            # Run in a different thread
            inner_excp = [False]

            def worker():
                """
                A worker function, running the testrunner in a separate thread
                """
                try:
                    test_runner.run(tests, context)
                    inner_excp[0] = True
                except Exception as excp:                                                    # pylint:disable=W0703
                    inner_excp[0] = excp
                # end try
            # end def worker

            thread1 = Thread(target = worker, name="UserThread 1")
            thread1.start()
            thread1.join()

            if global_exc[0] is not None:
                raise ValueError('Global exception should be None')
            # end if
        # end if
    # end def test_MonothreadDecorator
# end class TestRunnerTestCase


class MonoThreadTestRunnerTestCase(TestRunnerTestCase):
    """
    MonoThread testRunner test
    """

    @staticmethod
    def isAbstract():
        """
        @copydoc pyharness.test.coretest.TestRunnerTestCase.isAbstract
        """
        return False
    # end def isAbstract

    @staticmethod
    def _getTestRunnerClass():
        """
        Obtains a generator for the class under test

        @return The class for the TestRunner to test.
        """
        return MonoThreadTestRunner
    # end def _getTestRunnerClass
# end class MonoThreadTestRunnerTestCase


class MultiThreadTestRunnerTestCase(TestRunnerTestCase):
    """
    MultiThread testRunner test
    """

    @staticmethod
    def isAbstract():
        """
        @copydoc pyharness.test.coretest.TestRunnerTestCase.isAbstract
        """
        return False
    # end def isAbstract

    @staticmethod
    def _getTestRunnerClass():
        """
        Obtains a generator for the class under test

        @return The class for the TestRunner to test.
        """
        return MultiThreadTestRunner
    # end def _getTestRunnerClass

    def test_NoMonothreadDecorator(self):
        """
        Tests the non-monothread tests (not tagged with the @e monothread decorator).
        """

        test_runner_class = self._getTestRunnerClass()

        test_runner = test_runner_class()
        # Create 50 tests to run
        n_tests = 50
        quantum = 0.5
        tests = []
        discrepancies = [0]
        lock = Lock()

        class InnerTestCase(CoreTestCase):
            """
            Internal test, that always succeeds if i is even
            """

            # This overrides the global thread local data, which
            # would interact with the master test run
            # THREAD_LOCAL_DATA = local()
            __STATE = 0

            @classmethod
            def templateTest(cls):
                """
                A monothreaded test, that periodically checks the value of a counter
                """
                state = cls.__STATE
                cls.__STATE += 1
                sleep(quantum)
                if cls.__STATE != (state + 1):
                    with lock:
                        discrepancies[0] += 1
                    # end with
                # end if
            # end def templateTest
        # end class InnerTestCase

        # Test names _must_ different, in order to bypass the concurrent lock security
        for i in range(0, n_tests):
            test_name = 'test_Multithread_%d' % i
            setattr(InnerTestCase, test_name, InnerTestCase.templateTest)
            tests.append(InnerTestCase(test_name))
        # end for

        context = MockContext()

        test_runner.run(tests, context)

        self.assertNotEqual(0,
                            discrepancies[0],
                            "Suspicious multithread behavior: concurrent execution not detected")
    # end def test_NoMonothreadDecorator
# end class MultiThreadTestRunnerTestCase


class TestListenerTestCase(TestCase):
    """
    Base class for TestListener tests.

    This implements various tests on an instance of a TestListener.
    """

    MockContext = MockContext
    MyMockTest = staticmethod(instantiate_mock_test)

    @staticmethod
    def __exc_info():
        """
        Return a version of sys.exc_info() with the traceback frame minimised;

        Usually the top level of the traceback frame is not needed, as it only
        contains internal, pyharness-specific information.

        @return Tuple
        """
        import sys
        exctype, excvalue, tb = sys.exc_info()
        if sys.platform[:4] == 'java':  # tracebacks look different in Jython
            return exctype, excvalue, tb
        # end if
        newtb = tb.tb_next
        if newtb is None:
            return exctype, excvalue, tb
        # end if

        return exctype, excvalue, newtb
    # end def __exc_info

    _exc_info = __exc_info

    class MockTestResult(object):
        """
        A Mock implementation of a TestResult
        """

        def __init__(self, test):
            """
            A mock TestResult that checks the behavior of the TestListener

            @param  test [in] (TestCase) the test in which the case is instantiated
            """
            self.attachedTypes = {}
            self.detachedTypes = {}
            self._test = ref(test)
        # end def __init__

        def addListener(self, listenerType, listenerFunction, propagateException = False):      # pylint:disable=W0613
            """
            @copydoc pyharness.core.TestResult.addListener
            """
            self._test().assertEqual(False,
                                     listenerType in self.attachedTypes,
                                     "The listener %d is already attached" % listenerType)
            self.attachedTypes[listenerType] = listenerFunction
        # end def addListener

        def removeListener(self, listenerType, listenerFunction):
            """
            @copydoc pyharness.core.TestResult.removeListener
            """
            self._test().assertEqual(False,
                                     listenerType in self.detachedTypes,
                                     "The listener %d is already detached" % listenerType)
            self.detachedTypes[listenerType] = listenerFunction

            self._test().assertEqual(True,
                                     listenerType in self.attachedTypes,
                                     "The listener %d is already detached" % listenerType)
        # end def removeListener
    # end class MockTestResult

    def canRun(self, result, context):                                             # pylint:disable=W0613
        """
        @copydoc pyharness.core.TestCase.canRun
        """
        return not self.isAbstract()
    # end def canRun

    @staticmethod
    def isAbstract():
        """
        Used to detect whether the class is abtract, or contains an implementation.

        @return True if the class is abstract, False otherwise.
        """
        return True
    # end def isAbstract

    @staticmethod
    def _getTestListenerClass():
        """
        Obtains a generator for the class under test
        """
        raise NotImplementedError
    # end def _getTestListenerClass

    @staticmethod
    def _getKeywordArguments():
        """
        Obtains the keyword arguments for the class under test

        @return The keyword arguments for the class under test
        """
        return KeywordArguments.DEFAULT_ARGUMENTS
    # end def _getKeywordArguments

    def _prepareRun(self, listener_instance, tests):
        """
        Prepare a run.

        This is only needed for some testListeners

        @param  listener_instance [in] (TestListener) The TestListener under test
        @param  tests            [in] (list)         List of tests to run.
        """
        pass
    # end def _prepareRun

    def setUp(self):
        """
        Creates a temporary directory for output
        """
        TestCase.setUp(self)

        self.__tempDirPath = mkdtemp("", "test_%s" % self.id())
    # end def setUp

    def tearDown(self):
        """
        Cleans the temporary directory
        """

        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    def test_attachDetach(self):
        """
        Tests the attach and detach methods consistency
        """

        if not self.isAbstract():
            test_result = self.MockTestResult(self)

            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())
            listener_instance.attach(test_result)
            listener_instance.detach(test_result)
        # end if
    # end def test_attachDetach

    def test_StartStopRun(self):
        """
        Tests the startRun/stopRun method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            listener_instance.stopRun(context, True)
            listener_instance.startRun(context, True)
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_StartStopRun

    def test_StartStopRun_Erase(self):
        """
        Tests the startRun/stopRun method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            args = self._getKeywordArguments()
            args[KeywordArguments.KEY_ERASELOGS] = True
            listener_instance = listener_class(True, True, self.__tempDirPath, args)

            test_result = self.MockTestResult(self)
            context = self.MockContext()

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            listener_instance.stopRun(context, True)
            listener_instance.startRun(context, True)
            listener_instance.stopRun(test_result, False)
            args[KeywordArguments.KEY_ERASELOGS] = False
        # end if
    # end def test_StartStopRun_Erase

    def test_StartStopTest(self):
        """
        Tests the startTest/stopTest method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_StartStopTest", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)
                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_StartStopTest

    def test_Success(self):
        """
        Tests the addSuccess method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_Success", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                listener_instance.addSuccess(mock_test, None)

                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_Success

    def test_resetTest(self):
        """
        Tests the resetTest method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_ResetTest", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                listener_instance.addSuccess(mock_test, None)

                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)

            # Actual test of the resetTest method
            listener_instance.resetTest(mock_test, context)
        # end if
    # end def test_resetTest

    def test_veryLongTestId(self):
        """
        Tests the listener on a very long test identifier
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()

            class MockTestCase_0123456789012345678901234567890123456789(TestCase):
                """
                A mock test case, with a very long name
                """
                def __init__(self, methodName='runTest'):
                    """
                    Constructor
                    """
                    self.warning_occurred = False

                    super().__init__(methodName)
                # end def __ini__

                @staticmethod
                def test_0123456789012345678901234567890123456789():  # pylint:disable=C0103
                    """
                    A mock test
                    """
                    pass
                # end def test_0123456789012345678901234567890123456789
                
                def id(self):
                    mock_id = super(MockTestCase_0123456789012345678901234567890123456789, self).id()
                    return mock_id.replace('.TestListenerTestCase.test_veryLongTestId.<locals>', '')
                # def id
            # end class MockTestCase_0123456789012345678901234567890123456789

            mock_test = \
                MockTestCase_0123456789012345678901234567890123456789("test_0123456789012345678901234567890123456789")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                listener_instance.addSuccess(mock_test, None)

                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_veryLongTestId

    def test_Failure(self):
        """
        Tests the addFailure method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_Failure", "Mock test, with special chars: éàò")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                # create a fake assertionError
                try:
                    raise AssertionError("This is a sample assertion, with special chars: éàò")
                except AssertionError:
                    listener_instance.addFailure(mock_test, self.__exc_info())                 # pylint:disable=E1101
                # end try

                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_Failure

    def test_Error(self):
        """
        Tests the addError method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_Error", "Mock test, with special chars: éàò")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                # create a fake assertionError
                try:
                    raise AssertionError("This is a sample assertion, with special chars: éàò")
                except AssertionError:
                    listener_instance.addError(mock_test, self.__exc_info())                  # pylint:disable=E1101
                # end try

                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_Error

    def test_PerfData(self):
        """
        Tests the addPerformanceData method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_PerfData", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                listener_instance.addPerformanceData(mock_test, 'mockData1', 5)
                listener_instance.addPerformanceData(mock_test, 'mockData2', 1.5, "s")
                listener_instance.addPerformanceData(mock_test, 'mockData2', 7, "s")

                listener_instance.addSuccess(mock_test, None)
                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_PerfData

    def test_TestCase(self):
        """
        Tests the addTestCase
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_TestCase", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for index in range(3):
                listener_instance.startTest(mock_test)

                listener_instance.addTestCase(mock_test, "TESTCASE_NOM_%d" % index)
                listener_instance.addSuccess(mock_test, None)

                listener_instance.stopTest(mock_test)
            # end for

            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_TestCase

    # def test_Performance(self):
    #     """
    #     Tests the creation of 100 test notifications
    #     """
    #     if not self.isAbstract():
    #         listener_class = self._getTestListenerClass()
    #         listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())
    #
    #         test_result = self.MockTestResult(self)
    #         context = MockContext()
    #
    #         test_successes = [instantiate_mock_test("test_MockSuccess_%d" % i,
    #                                                 "Mock success %d" % i) for i in range(75)]
    #         test_failures = [instantiate_mock_test("test_MockFailure_%d" % i,
    #                                                "Mock failure %d" % i) for i in range(20)]
    #         test_errors = [instantiate_mock_test("test_MockError_%d" % i,
    #                                              "Mock error %d" % i) for i in range(5)]
    #
    #         from time import time
    #         tock = time()
    #
    #         all_tests = []
    #         all_tests.extend(test_successes)
    #         all_tests.extend(test_failures)
    #         all_tests.extend(test_errors)
    #
    #         # Now that the listener has been created, simulate a call
    #         listener_instance.startRun(context, False)
    #         self._prepareRun(listener_instance, all_tests)
    #         for testCase in test_successes:
    #             listener_instance.startTest(testCase)
    #             listener_instance.addSuccess(testCase)
    #             listener_instance.stopTest(testCase)
    #         # end for
    #
    #         for testCase in test_failures:
    #             listener_instance.startTest(testCase)
    #
    #             # create a fake assertionError
    #             try:
    #                 raise AssertionError("This is a sample assertion")
    #             except AssertionError:
    #                 listener_instance.addFailure(testCase, self.__exc_info())                  # pylint:disable=E1101
    #             # end try
    #
    #             listener_instance.stopTest(testCase)
    #         # end for
    #
    #         for testCase in test_errors:
    #             listener_instance.startTest(testCase)
    #
    #             # create a fake assertionError
    #             try:
    #                 raise AssertionError("This is a sample assertion")
    #             except AssertionError:
    #                 listener_instance.addError(testCase, self.__exc_info())                    # pylint:disable=E1101
    #             # end try
    #
    #             listener_instance.stopTest(testCase)
    #         # end for
    #
    #         listener_instance.stopRun(test_result, False)
    #
    #         tick = time()
    #
    #         # Log performance data for this run
    #         key = "FullRun_%s_%d_tests" % (listener_class.__name__,
    #                                        len(test_successes) + len(test_failures) + len(test_errors))
    #         value = (tick - tock)
    #         # self.addPerformanceData(key, value, "s")
    #     # end if
    # # end def test_Performance

    def test_Log(self):
        """
        Tests the logging of some data
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()

            test_logs = [(self.MyMockTest("test_MockLog_%d" % i, "Mock log %d" % i), i) for i in _ALL_LEVELS]

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [testLog[0] for testLog in test_logs])
            for testCase, logLevel in test_logs:
                listener_instance.startTest(testCase)
                listener_instance.log(testCase, logLevel, "Testing log level %d" % logLevel)
                listener_instance.addSuccess(testCase)
                listener_instance.stopTest(testCase)
            # end for

            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_Log

    def test_Log_LargeValue(self):
        """
        Tests the logging of large data
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()

            test_logs = [(self.MyMockTest("test_MockLog_%d" % i, "Mock log %d" % i), i) for i in [_LEVEL_RAW]]

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [testLog[0] for testLog in test_logs])
            for testCase, logLevel in test_logs:
                log_data = 'X'
                listener_instance.startTest(testCase)
                for _ in range(1, 15):
                    listener_instance.log(testCase, logLevel, "Testing log length: %d" % len(log_data))
                    listener_instance.log(testCase, logLevel, log_data)
                    log_data *= 2
                # end for
                listener_instance.addSuccess(testCase)
                listener_instance.stopTest(testCase)
            # end for

            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_Log_LargeValue

    def test_LogInfo(self):
        """
        Tests the log at info level method
        """
        if not self.isAbstract():
            listener_class = self._getTestListenerClass()
            listener_instance = listener_class(True, True, self.__tempDirPath, self._getKeywordArguments())

            test_result = self.MockTestResult(self)
            context = self.MockContext()
            mock_test = self.MyMockTest("test_LogInfo", "Mock test")

            # Now that the listener has been created, simulate a call
            listener_instance.startRun(context, False)
            self._prepareRun(listener_instance, [mock_test])
            for unused in range(3):
                listener_instance.startTest(mock_test)

                listener_instance.log(mock_test, _LEVEL_INFO, 'log_value: 0x12345678')
                listener_instance.addSuccess(mock_test, None)

                listener_instance.stopTest(mock_test)
            # end for
            listener_instance.stopRun(test_result, False)
        # end if
    # end def test_LogInfo
# end class TestListenerTestCase


class NormalTestsTestCase(TestCase):
    """
    Test case containing only 'normal' test cases
    """
    SYNCHRONIZATION_LOCK = RLock()
    currentCount = 0

    def test_0Starter(self):                                               # pylint:disable=R0201
        """
        Initializer
        """
        with self.SYNCHRONIZATION_LOCK:
            NormalTestsTestCase.currentCount = 0
        # end with
    # end def test_0Starter

    def test_1Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_1Increment

    def test_2Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_2Increment

    def test_3Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_3Increment

    def test_4Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_4Increment

    def test_5Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_5Increment

    def test_6Ender(self):
        """
        Waits 5 seconds for the other tests to terminate, and check
        """
        sleep(1)

        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(5,
                             NormalTestsTestCase.currentCount,
                             "Tests incorrectly run")
        # end with
    # end def test_6Ender

    def _incrementCount(self):
        """
        First instance of a test.
        """
        with self.SYNCHRONIZATION_LOCK:
            NormalTestsTestCase.currentCount += 1
        # end with
    # end def _incrementCount
# end class NormalTestsTestCase


class SubTestsTestCase(TestCase):
    """
    Test case containing only 'normal' test cases
    """
    SYNCHRONIZATION_LOCK = RLock()
    currentCount = 0

    def setUp(self):
        """
        Resets the setUp count
        """
        with self.SYNCHRONIZATION_LOCK:
            SubTestsTestCase.currentCount = 0
        # end with
    # end def setUp

    def subTest_0Starter(self):                                                            # pylint:disable=R0201
        """
        Initializer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(0,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
            SubTestsTestCase.currentCount += 1
        # end with
    # end def subTest_0Starter

    def subTest_1Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(1,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
            SubTestsTestCase.currentCount += 1
        # end with
    # end def subTest_1Increment

    def subTest_2Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(2,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
            SubTestsTestCase.currentCount += 1
        # end with
    # end def subTest_2Increment

    def subTest_3Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(3,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
            SubTestsTestCase.currentCount += 1
        # end with
    # end def subTest_3Increment

    def subTest_4Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(4,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
            SubTestsTestCase.currentCount += 1
        # end with
    # end def subTest_4Increment

    def subTest_5Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(5,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
            SubTestsTestCase.currentCount += 1
        # end with
    # end def subTest_5Increment

    def subTest_6Ender(self):
        """
        Waits 1 seconds for the other tests to terminate, and check
        """
        sleep(1)

        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(6,
                             SubTestsTestCase.currentCount,
                             "Unexpected setUp count")
        # end with
    # end def subTest_6Ender
# end class SubTestsTestCase


class MixedTestsTestCase(TestCase):
    """
    Mixed tests, containing both normal and sub tests
    """
    SYNCHRONIZATION_LOCK = RLock()
    currentCount = 0
    setUpCount = 0

    def test_0Starter(self):                                                             # pylint:disable=R0201
        """
        Initializer
        """
        with self.SYNCHRONIZATION_LOCK:
            MixedTestsTestCase.currentCount = 0
            MixedTestsTestCase.setUpCount = 0
        # end with
    # end def test_0Starter

    def test_1Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_1Increment

    def test_2Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_2Increment

    def test_3Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_3Increment

    def test_4Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_4Increment

    def test_5Increment(self):
        """
        Incrementer
        """
        self._incrementCount()
    # end def test_5Increment

    def test_6Ender(self):
        """
        Waits 1 seconds for the other tests to terminate, and check
        """
        sleep(1)

        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(5,
                             MixedTestsTestCase.currentCount,
                             "Tests incorrectly run")

            self.assertEqual(0,
                             MixedTestsTestCase.setUpCount,
                             "setUp incorrectly called")
        # end with
    # end def test_6Ender

    def _incrementCount(self):
        """
        First instance of a test.
        """
        with self.SYNCHRONIZATION_LOCK:
            MixedTestsTestCase.currentCount += 1
        # end with
    # end def _incrementCount

    def setUp(self):
        """
        Resets the setUp count
        """
        with self.SYNCHRONIZATION_LOCK:
            MixedTestsTestCase.setUpCount = 0
        # end with
    # end def setUp

    def subTest_0Starter(self):                                              # pylint:disable=R0201
        """
        Initializer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(0,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
            MixedTestsTestCase.setUpCount += 1
        # end with
    # end def subTest_0Starter

    def subTest_1Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(1,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
            MixedTestsTestCase.setUpCount += 1
        # end with
    # end def subTest_1Increment

    def subTest_2Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(2,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
            MixedTestsTestCase.setUpCount += 1
        # end with
    # end def subTest_2Increment

    def subTest_3Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(3,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
            MixedTestsTestCase.setUpCount += 1
        # end with
    # end def subTest_3Increment

    def subTest_4Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(4,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
            MixedTestsTestCase.setUpCount += 1
        # end with
    # end def subTest_4Increment

    def subTest_5Increment(self):
        """
        Incrementer
        """
        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(5,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
            MixedTestsTestCase.setUpCount += 1
        # end with
    # end def subTest_5Increment

    def subTest_6Ender(self):
        """
        Waits 0.5 seconds for the other tests to terminate, and check
        """
        sleep(0.5)

        with self.SYNCHRONIZATION_LOCK:
            self.assertEqual(6,
                             MixedTestsTestCase.setUpCount,
                             "Unexpected setUp count")
        # end with
    # end def subTest_6Ender
# end class MixedTestsTestCase


# This MUST stay global for the static analysis to work
MOCK_TESTCASE = 'MOCK_TESTCASE'


class TestCaseTestCase(TestCase):
    """
    TestCase class's autotests
    """

    class MockTestCase(CoreTestCase):
        """
        A test class
        """
        def runTest(self):
            """
            Dummy test
            """
            pass
        # end def runTest
    # end class MockTestCase

    CLASS = MockTestCase

    def testAssertEqual(self):
        """
        Tests of the assertEqual method.
        """
        instance = self.CLASS()
        try:
            instance.assertEqual("1234",
                                 "1234",
                                 "Values should be equal")
        except TestException:
            raise TestException(TYPE_FAILURE, "assertEqual should not have raised an exception")
        # end try

        try:
            instance.assertEqual("123411111111111111111",
                                 "123511111111111111111",
                                 "Values should not be equal !",
                                 maxDisplayLength=8)
        except TestException:
            pass
        else:
            raise TestException(TYPE_FAILURE, "assertEqual should have raised an exception")
        # end try
    # end def testAssertEqual

    def testAssertTrue(self):
        """
        Tests of the assertTrue method.
        """
        instance = self.CLASS()
        try:
            instance.assertTrue(True,
                                "This should be true")
        except TestException:
            raise TestException(TYPE_FAILURE, "assertTrue should not have raised an exception")
        # end try

        try:
            instance.assertEqual(1,
                                 "This should not be true")
        except TestException:
            pass
        else:
            raise TestException(TYPE_FAILURE, "assertTrue should have raised an exception")
        # end try
    # end def testAssertTrue

    def testAssertFalse(self):
        """
        Tests of the assertFalse method.
        """
        instance = self.CLASS()
        try:
            instance.assertFalse(False,
                                 "This should be false")
        except TestException:
            raise TestException(TYPE_FAILURE, "assertFalse should not have raised an exception")
        # end try

        try:
            instance.assertTrue(0,
                                "This should not be false")
        except TestException:
            pass
        else:
            raise TestException(TYPE_FAILURE, "assertFalse should have raised an exception")
        # end try
    # end def testAssertFalse

    def testTestCase(self):
        """
        Smoke test for testCaseChecked
        """
        instance = self.CLASS()
        instance.checkTestCase(MOCK_TESTCASE)
    # end def testTestCase
# end class TestCaseTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
