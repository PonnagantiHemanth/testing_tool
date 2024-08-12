#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyharness.extensions

@brief Extensions of the core TestCases

This module contains the base implementation of extension cases.

These base implementations:
- Initialize the logs
- Implement the level filtering mechanism.

@author christophe.roquebert

@date   2018/06/05
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.importutils import importFqn
from pylibrary.tools.logger import Logger
from pylibrary.tools.logger import LoggerProvider
from pylibrary.tools.tracebacklog import TracebackLogWrapper
from pysetup import PROJECT_NAME                                # @UnresolvedImport # pylint:disable=E0611
from pyharness.consts import PROGRAM_NAME
from pyharness.consts import PROGRAM_VERSION
from pyharness.context import FeaturesProvider
from pyharness.core import TYPE_BUG
from pyharness.core import TestCase
from pyharness.core import TestException
from pyharness.core import TestLoader
from pyharness.core import TestSuite
from pyharness.core import _LEVEL_INFO
from pyharness.core import _LEVEL_DEBUG
from pyharness.core import _LEVEL_ERROR
from pyharness.core import _LEVEL_RAW
from pyharness.core import _LEVEL_SEPARATOR
from pyharness.core import _LEVEL_TITLE1
from pyharness.core import _LEVEL_TITLE2
from pyharness.core import _LEVEL_TITLE3
from pyharness.core import _LEVEL_TRACE
from pyharness.core import _MASK_ALWAYS
from pyharness.tools.tag import Tag
from os.path import dirname
from random import seed
from time import localtime
from time import strftime
from time import time
from weakref import ref
from enum import Enum


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class WarningLevel(Enum):
    NO_WARNING = 0
    IMPORTANT = 1
    ROBUSTNESS = 2
# end class WarningLevel


class Level(Tag):
    """
    Function decorator, that associates a level with a function definition.

    This should be used in tests, on test methods, to declare the test level.

    Example:
    @code
    from pyharness.extensions import PyHarnessCase
    from pyharness.extensions import level
    class MyTest(PyHarnessCase):

        @level("minimal")
        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example
    # end class MyTest
    @endcode

    The above code is equivalent to:
    @code
    from pyharness.extensions import PyHarnessCase
    from pyharness.extensions import level
    class MyTest(PyHarnessCase):

        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example

        levelAssigner = Level.__call__(level, "minimal")
        test_Example = levelAssigner(test_Example)
    # end class MyTest
    @endcode
    """

    def __init__(self):
        """
        Constructor
        """
        super(Level, self).__init__('level')
    # end def __init__

    def get_levels(self, f=None):
        """
        Obtains the list of levels for which a function is registered.

        @param f [in] (FunctionType) The function to check, None to obtain _all_ levels
        @return The list of registered levels
        """
        return super(Level, self).getTags(f=f)
    # end def getLevels

    def has_level(self, f, levels):
        """
        Tests whether a function is associated with a set of levels.

        @param  f      [in] (MethodType) The MethodType object to test
        @param  levels [in] (tuple)      The list of levels to test against

        @return True if the function has been registered with one of the levels
                with the @@level decorator
        """
        return super(Level, self).hasTag(f, levels)
    # end def hasLevel

    def defines_level(self, f):
        """
        Tests whether a function has defined a level.

        @param  f [in] (FunctionType) The function to test

        @return True if the function has defined a level with the @@level
                decorator
        """
        return super(Level, self).definesTag(f)
    # end def definesLevel

    def restrict_levels(self, levels):
        """
        Restricts the levels to a list of pre-defined values

        @param levels [in] (list) List of levels to restrict to.
        """
        super(Level, self).restrictTags(levels)
    # end def restrictLevels
# end class Level


# The global level monitor. Its name should be ignored by pylint
level = Level()                                         # pylint: disable=C0103


class DelegateLogger(Logger):
    """
    A delegate logger, used to break cycles in the various libraries.

    This ensures that even if the object returned by getLogger is kept
    in an attribute of the test instance, this does not introduce cycles
    that will prevent the garbage collector from reclaiming memory.
    """

    def __init__(self, next):                                           # @ReservedAssignment # pylint:disable=W0622
        """
        Constructor

        @param next [in] (Logger) The logger to delegate the calls to.
        """
        super(DelegateLogger, self).__init__()

        self._next = ref(next)
    # end def __init__

    def logError(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logError
        """
        return self._next().logError(msg, *args, **kwargs)
    # end def logError

    def logTitle1(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle1
        """
        return self._next().logTitle1(msg, *args, **kwargs)
    # end def logTitle1

    def logTitle2(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle2
        """
        return self._next().logTitle2(msg, *args, **kwargs)
    # end def logTitle2

    def logTitle3(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle3
        """
        return self._next().logTitle3(msg, *args, **kwargs)
    # end def logTitle3

    def logSeparator(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logSeparator
        """
        return self._next().logSeparator(msg, *args, **kwargs)
    # end def logSeparator

    def logTrace(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTrace
        """
        return self._next().logTrace(msg, *args, **kwargs)
    # end def logTrace

    def logDebug(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logDebug
        """
        return self._next().logDebug(msg, *args, **kwargs)
    # end def logDebug

    def logRaw(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logRaw
        """
        return self._next().logRaw(msg, *args, **kwargs)
    # end def logRaw

    def logInfo(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logInfo
        """
        return self._next().logInfo(msg, *args, **kwargs)
    # end def logInfo

    def log(self, logLevel, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.log
        """
        return self._next().log(logLevel, msg, *args, **kwargs)
    # end def log

    def addPerformanceData(self, key, value, unit=None):
        """
        @copydoc pyharness.core.TestCase.addPerformanceData
        """
        return self._next().addPerformanceData(key, value, unit)
    # end def addPerformanceData
# end class DelegateLogger


class PyHarnessCase(TestCase, Logger, LoggerProvider, FeaturesProvider):                         # pylint:disable=R0901
    """
    PyHarnessCase implementation

    Provides additional testing methods, useful in a feature context.
    """
    WARNING_LEVEL = WarningLevel.IMPORTANT

    def __init__(self, methodName='runTest'):
        """
        Constructor

        @option methodName [in] (str) Name of the method to launch
        """
        TestCase.__init__(self, methodName=methodName)
        Logger.__init__(self)
        LoggerProvider.__init__(self)
        FeaturesProvider.__init__(self)

        self.__logger = None
        self._logging_done = False
    # end def __init__

    def setUp(self):
        """
        Initialization
        """
        TestCase.setUp(self)

        if not self._logging_done:
            # Log the test description
            self.log(_LEVEL_TRACE + _MASK_ALWAYS,
                     '[Summary] %s\n' % (self.shortDescription()),)

            self.log(_LEVEL_TRACE + _MASK_ALWAYS,
                     '[Description] %s\n' % (self.fullDescription(),))

            # Log the test date and time
            self.log(_LEVEL_TRACE + _MASK_ALWAYS,
                     strftime('[DateTime] %Y-%m-%d %H:%M:%S\n', localtime()))

            # log the program name and version
            self.log(_LEVEL_TRACE + _MASK_ALWAYS,
                     '[Project Info]\n - Project %s\n - Name    %s\n - Version %s\n'
                     % (PROJECT_NAME,
                        PROGRAM_NAME,
                        PROGRAM_VERSION))

            # Check the context
            context = self.getContext()
            if context is not None:
                # Log the test configuration (source/target)
                context = self.getContext()

                product = context.getCurrentProduct()
                variant = context.getCurrentVariant()
                target = context.getCurrentTarget()
                self.log(_LEVEL_TRACE + _MASK_ALWAYS,
                         '[Settings]\n - Product %s\n - Variant %s\n - Target  %s\n'
                         % (product,
                            variant,
                            target))
            # end if

            # Initialize the random seed with the checksum of the test name
            # This is according to Ticket #494
            seed_value = 0
            if context is not None:
                runtime = self.getFeatures().RUNTIME
                if hasattr(runtime, 'F_RandSeed'):
                    seed_value = runtime.F_RandSeed
                # end if
            # end if

            if seed_value is None:
                seed_value = int(hash(time()))
            elif seed_value == 0:
                seed_value = int(hash(self.id()))
            else:
                seed_value = int(seed_value)
            # end if

            seed(seed_value)
            self.logInfo('\n - HexList Random    %d\n' % (seed_value,))
            self._logging_done = True
        # end if
    # end def setUp

    def tearDown(self):
        """
        Cleanup
        """
        TestCase.tearDown(self)
    # end def tearDown

    def getLogger(self):
        """
        @copydoc pylibrary.tools.logger.LoggerProvider.getLogger
        """
        if self.__logger is None:
            self.__logger = DelegateLogger(self)
        # end if

        return self.__logger
    # end def getLogger

    def getFeatures(self):
        """
        @copydoc pyharness.context.FeaturesProvider.getFeatures
        """
        return self.getContext().getFeatures()
    # end def getFeatures

    @classmethod
    def assertBug(cls, bugFeature, checkIfBug, checkIfNotBug, message):
        """
        Check if an identified bug has been found

        @param  bugFeature    [in] (bool) Condition to recognize the bug as referenced
        @param  checkIfBug    [in] (bool) The check performed if the bug is expected
        @param  checkIfNotBug [in] (bool) The check performed if the bug is NOT expected
        @param  message       [in] (str)  Message to display if an error occurs
        """

        assert not checkIfBug and checkIfNotBug, 'Undecidable bug: Both found and not found'
        assert checkIfBug or checkIfNotBug, 'Undecidable bug: Neither found nor not found'

        if (bugFeature and checkIfNotBug) or (not bugFeature and checkIfBug):
            raise TestException(TYPE_BUG, message)
        # end if
    # end def assertBug

    def logError(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logError
        """
        self.log(_LEVEL_ERROR, msg, *args, **kwargs)
    # end def logError

    def logTitle1(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle1
        """
        self.log(_LEVEL_TITLE1, msg, *args, **kwargs)
    # end def logTitle1

    def logTitle2(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle2
        """
        self.log(_LEVEL_TITLE2, msg, *args, **kwargs)
    # end def logTitle2

    def logTitle3(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle3
        """
        self.log(_LEVEL_TITLE3, msg, *args, **kwargs)
    # end def logTitle3

    def logSeparator(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logSeparator
        """
        self.log(_LEVEL_SEPARATOR, msg, *args, **kwargs)
    # end def logSeparator

    def logTrace(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logTrace
        """
        self.log(_LEVEL_TRACE, msg, *args, **kwargs)
    # end def logTrace

    def logDebug(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logDebug
        """
        self.log(_LEVEL_DEBUG, msg, *args, **kwargs)
    # end def logDebug

    def logRaw(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logRaw
        """
        self.log(_LEVEL_RAW, msg, *args, **kwargs)
    # end def logRaw

    def logInfo(self, msg, *args, **kwargs):
        """
        @copydoc pylibrary.tools.logger.Logger.logInfo
        """
        self.log(_LEVEL_INFO, msg, *args, **kwargs)
    # end def logInfo

    def log_traceback_as_warning(
            self, supplementary_message=None, warning_level=WarningLevel.IMPORTANT, force_console_print=False):
        exception_stack = TracebackLogWrapper.get_traceback_stack()
        message = supplementary_message + "\n" + exception_stack if supplementary_message is not None \
            else exception_stack
        self.log_warning(message=message, warning_level=warning_level, force_console_print=force_console_print)
    # end log_traceback_as_warning

    def log_warning(self, message, warning_level=WarningLevel.IMPORTANT, force_console_print=False):
        message_to_log = f"\n========== Warning level {warning_level.name} - START ==========\n"
        message_to_log += message
        message_to_log += f"\n=========== Warning level {warning_level.name} - END ===========\n"
        if force_console_print:
            print(message_to_log)
        # end if

        self.logTrace(msg=message_to_log)

        if warning_level.value <= self.WARNING_LEVEL.value:
            self.warning_occurred = True
        # end if
    # end log_warning
# end class PyHarnessCase


class PyHarnessSuite(TestSuite):
    """
    Utility class that wraps a test suite, and notifies
    the listeners of the suite start and end.
    """

    def run(self, result=None, context=None):
        """
        @copydoc pyharness.core.TestSuite.run
        """
        if self.canRun(result, context):
            result.startTest(self)
            self.runTests(result, context)
            result.stopTest(self)
        # end if
    # end def run

    __call__ = run

    def runTests(self, result, context):
        """
        Runs all the tests in the test suite.

        @param result  [inout] (TestResult) The test result that will collect the results.
        @param context [in]    (Context)    The context in which the tests are run.
        """
        raise NotImplementedError
    # end def runTests
# end class PyHarnessSuite


class DiscoveryTestSuite(TestSuite):
    """
    The DiscoveryTestSuite audits the package it is declared in, and looks for
    TestCase-derived classes.
    """

    def __init__(self, *args, **kwargs):                                               # pylint:disable=W0613
        """
        Constructor

        @param args   [in] (tuple) The arguments, discarded
        @param kwargs [in] (dict)  The keyword arguments, discarded
        """

        # The __file__ attribute MUST be accessed for a proper discovery
        # It does not guarantee zip-safety for eggs.
        # As this should never be used to discover tests within eggs,
        # it should be ok to use the following trick to disable zip-non-safety
        # detection
        key = '__'
        key += 'file'
        key += '__'

        path = dirname(getattr(importFqn(self.__class__.__module__), key))
        name = "%s.%s" % (self.__class__.__module__, self.__class__.__name__, )
        root_fqn = '.'.join(self.__class__.__module__.rsplit('.')[:-1]) + '.'

        tests = TestLoader.findTestsInSrcPath(
            path,
            rootFQN=root_fqn,
            classPredicate=lambda c: (c is not self.__class__) and (c.__module__ not in ('pyharness.core',
                                                                                         'pyharness.extensions',
                                                                                         'pyharness.device',
                                                                                         'pyharness.debugger')),
            useTestRunner=True,
            rootTestRunner=True,
            aggregateToPyHarness=False)

        TestSuite.__init__(self, tests, name)
    # end def __init__
# end class DiscoveryTestSuite

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
