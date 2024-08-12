#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.tools.test.base

@brief  Testing module for base

@author christophe Roquebert

@date   2018/06/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.system.device            import BaseSmartDevice
from pylibrary.tools.logger             import Logger
from pylibrary.tools.test.logger_test        import LoggerTestCase
from pyharness.core                     import _LEVEL_DEBUG
from pyharness.core                     import _LEVEL_ERROR
from pyharness.core                     import _LEVEL_INFO
from pyharness.core                     import _LEVEL_RAW
from pyharness.core                     import _LEVEL_SEPARATOR
from pyharness.core                     import _LEVEL_TITLE1
from pyharness.core                     import _LEVEL_TITLE2
from pyharness.core                     import _LEVEL_TITLE3
from pyharness.core                     import _LEVEL_TRACE
from pyharness.output.vblogui           import VBLogFormatter as LogFormatter
from pyharness.tools.base               import LeveledLogger
from pyharness.tools.base               import Provider
from pyharness.tools.base               import StreamLogger
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ProviderTestCase(TestCase):
    '''
    Testing class for Provider
    '''
    RefClass = Provider

    @classmethod
    def _createInstance(cls, context    = None,
                             logger     = None):
        '''
        Create an instance of referenced class

        @param  context [in] (Context) The context to wrap
        @option logger  [in] (Logger)  The current logger

        @return (object) Instance of referenced class
        '''
        callCollector = []
        if (context is None):
            context = cls.MockContext(callCollector)

        else:
            context.callCollector = callCollector

        # end if

        if (logger is None):
            logger = cls.MockLogger(callCollector)

        else:
            logger.callCollector = callCollector

        # end if

        return cls.RefClass(context, logger), callCollector
    # end def _createInstance

    class CollectorMixin(object):
        '''
        A Mixin collecting method calls and providing dummy answers
        '''

        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            self.collectedCalls = callCollector
        # end def __init__

        def stub(self, methodName,
                       returnValue = None):
            '''
            Defines a new stub, to replace an instance method.

            @param  methodName  [in] (str) Method name to stub
            @option returnValue [in] (object) Method return value
            '''
            def sink(*args, **kwargs):
                '''
                Method sink, to collect calls and return a fixed value

                @option args   [in] (tuple) Positional arguments
                @option kwargs [in] (tuple) Keyword arguments

                @return The stubbed return value
                '''
                self.collectedCalls.append((methodName, args, kwargs))
                return returnValue
            # end def sink

            setattr(self, methodName, sink)
        # end def stub
    # end class CollectorMixin

    class MockLogger(Logger, CollectorMixin):                                                                           # pylint:disable=W0223
        '''
        A logger collecting method calls to the log API
        '''
        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            Logger.__init__(self)
            ProviderTestCase.CollectorMixin.__init__(self, callCollector = callCollector)

            self.stub('open')
            self.stub('close')
            self.stub('logTitle1')
            self.stub('logTitle2')
            self.stub('logTitle3')
            self.stub('logError')
            self.stub('logTrace')
            self.stub('logDebug')
            self.stub('log')
            self.stub('logRaw')
            self.stub('logInfo')
            self.stub('logSeparator')
            self.stub('addPerformanceData')
        # end def __init__
    # end class MockLogger

    class MockContext(CollectorMixin):
        '''
        A context collecting method calls to the log API
        '''
        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            super(ProviderTestCase.MockContext, self).__init__(callCollector)

            self.device = BaseSmartDevice(10)

            self.stub('getDevice', self.device)
            self.stub('getFeatures', {'F_Feature': 1234})

        # end def __init__
    # end class MockContext

    def testGetLogger(self):
        '''
        Tests getLogger method
        '''
        expected = self.MockLogger([])
        instance, _ = self._createInstance(logger = expected)

        self.assertEqual(expected,
                         instance.getLogger(),
                         'Wrong logger returned')

    # end def testGetLogger

    def testGetContext(self):
        '''
        Tests getContext method
        '''
        expected = self.MockContext([])
        instance, _ = self._createInstance(context = expected)

        self.assertEqual(expected,
                         instance.getContext(),
                         'Wrong context returned')

    # end def testGetContext

    # TODO enable
    def _testGetDevice(self):
        '''
        Tests getDevice method
        '''
        instance, callCollector = self._createInstance()

        del callCollector[:]
        self.assertEqual(10,
                         instance.getDevice().number,
                         'Wrong device returned')

        self.assertTrue(('getDevice', (0, ), {}) in callCollector,
                        'getDevice not called on back-end')

        del callCollector[:]
        self.assertEqual(10,
                         instance.getDevice().number,
                         'Wrong device returned')

        self.assertEqual([],
                         callCollector,
                         'No call on back-end expected')

    # end def testGetDevice

    def testGetFeatures(self):
        '''
        Tests getFeatures method
        '''
        instance, callCollector = self._createInstance()

        del callCollector[:]
        self.assertEqual({'F_Feature': 1234},
                         instance.getFeatures(),
                         'Wrong features returned')

        self.assertTrue(('getFeatures', tuple(), {}) in callCollector,
                        'getFeatures not called on back-end')

    # end def testGetFeatures

    METHODS_PARAMETERS = (('close', None),
                          ('logTitle1', ('message',)),
                          ('logTitle2', ('message',)),
                          ('logTitle3', ('message',)),
                          ('logError', ('message',)),
                          ('logTrace', ('message',)),
                          ('logSeparator', ('message',)),
                          ('logDebug', ('message',)),
                          ('log', (1, 'message')),
                          ('logRaw', ('message',)),
                          ('logInfo', ('message',)),
                          )

    def testLoggerMethods(self):
        '''
        Tests method redirection of logger
        '''
        instance, callCollector = self._createInstance()

        for methodName, parameters in self.METHODS_PARAMETERS:
            del callCollector[:]
            if (parameters is None):
                getattr(instance, methodName)()
            else:
                getattr(instance, methodName)(*parameters)
            # end if

            parameters = tuple() if parameters is None else parameters
            self.assertTrue(('%s' % methodName, parameters, {}) in callCollector,
                            '%s not called on back-end' % methodName)

        # end for

    # end def testLoggerMethods

# end class ProviderTestCase

class StreamLoggerTestCase(LoggerTestCase):
    '''
    Tests StreamLogger class
    '''
    RefClass = StreamLogger

    class TestStream(object):
        '''
        Test stream
        '''
        STATE_OPEN      = 'open'
        STATE_CLOSED    = 'closed'

        def __init__(self):
            '''
            Constructor
            '''
            super(StreamLoggerTestCase.TestStream, self).__init__()

            self._log = None
            self._state = self.STATE_OPEN

        # end def __init__

        def getLastLog(self):
            '''
            Get last log

            @return (string) Last log
            '''
            return self._log
        # end def getLastLog

        lastLog = property(getLastLog)

        def getState(self):
            '''
            Get the state of the stream

            @return (string) State of the stream
            '''
            return self._state
        # end def getState

        state = property(getState)

        def write(self, log):
            '''
            Memorization of the log

            @param  log [in] (string) Log to memorize
            '''
            self._log = log
        # end def write

        def close(self):
            '''
            Close the stream
            '''
            self._state = self.STATE_CLOSED

        # end def close
    # end class TestStream

    def _createInstance(self, stream        = None,                                                                     # pylint:disable=W0221
                              needNewLine   = False,
                              needsClose    = False):
        '''
        @copydoc pylibrary.tools.test.logger.LoggerTestCase._createInstance

        @option stream      [in] (stream) The output stream
        @option needNewLine [in] (bool) Whether a newline should be inserted for each log action.
        @option needsClose  [in] (bool) Whether the stream is closed on exit
        '''
        if (stream is None):
            self.stream = StreamLoggerTestCase.TestStream()

        else:
            self.stream = stream                                                                                        # pylint:disable=W0201

        # end if

        return self.RefClass(self.stream, needNewLine, needsClose)
    # end def _createInstance

    def testLogSeparator(self):
        '''
        Tests logSeparator method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logSeparator(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_SEPARATOR, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogSeparator

    def testLogTitle1(self):
        '''
        Tests logTitle1 method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logTitle1(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_TITLE1, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogTitle1

    def testLogTitle2(self):
        '''
        Tests logTitle2 method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logTitle2(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_TITLE2, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogTitle2

    def testLogTitle3(self):
        '''
        Tests logTitle3 method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logTitle3(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_TITLE3, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogTitle3

    def testLogTrace(self):
        '''
        @copydoc pylibrary.tools.test.logger.LoggerTestCase.testLogTrace
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logTrace(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_TRACE, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogTrace

    def testLogRaw(self):
        '''
        Tests logRaw method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logRaw(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_RAW, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogRaw

    def testLogInfo(self):
        '''
        Tests logInfo method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logInfo(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_INFO, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogInfo

    def testLogError(self):
        '''
        Tests logError method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logError(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_ERROR, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogError

    def testLogDebug(self):
        '''
        Tests logDebug method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.logDebug(expected)

        self.assertEqual(LogFormatter.format(_LEVEL_DEBUG, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLogDebug

    def testLog(self):
        '''
        Tests log method
        '''
        instance = self._createInstance()

        expected = 'expected message'

        instance.log(1, expected)

        self.assertEqual(LogFormatter.format(1, expected),
                         self.stream.lastLog,
                         'Wrong logging')

        # With args
        message  = 'expected %s'
        args     = ('message', )
        expected = 'expected message'

        instance.log(1, message, *args)

        self.assertEqual(LogFormatter.format(1, expected),
                         self.stream.lastLog,
                         'Wrong logging')

        # With kwargs
        message  = 'expected %(key)s'
        kwargs   = {'key': 'message'}
        expected = 'expected message'

        instance.log(1, message, **kwargs)

        self.assertEqual(LogFormatter.format(1, expected),
                         self.stream.lastLog,
                         'Wrong logging')

    # end def testLog

    def testClose(self):
        '''
        Tests the close method
        '''
        instance = self._createInstance()

        instance.close()

        self.assertEqual(StreamLoggerTestCase.TestStream.STATE_OPEN,
                         self.stream.state,
                         'Wrong stream state')

        # Close of the stream
        instance = self._createInstance(needsClose = True)

        instance.close()

        self.assertEqual(StreamLoggerTestCase.TestStream.STATE_CLOSED,
                         self.stream.state,
                         'Wrong stream state')

    # end def testClose

# end class StreamLoggerTestCase

class LeveledLoggerTestCase(TestCase):
    '''
    Tests for LeveledLogger class
    '''
    RefClass = LeveledLogger

    class CollectorMixin(object):
        '''
        A Mixin collecting method calls and providing dummy answers
        '''

        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            self.collectedCalls = callCollector
        # end def __init__

        def stub(self, methodName, returnValue = None):
            '''
            Defines a new stub, to replace an instance method.

            @param  methodName  [in] (str) Method name to stub
            @option returnValue [in] (object) Method return value
            '''
            def sink(*args, **kwargs):
                '''
                Method sink, to collect calls and return a fixed value

                @option args   [in] (tuple) Positional arguments
                @option kwargs [in] (tuple) Keyword arguments

                @return The stubbed return value
                '''
                self.collectedCalls.append((methodName, args, kwargs))
                return returnValue
            # end def sink

            setattr(self, methodName, sink)
        # end def stub
    # end class CollectorMixin

    class MockLogger(Logger, CollectorMixin):                                                                           # pylint:disable=W0223
        '''
        A logger collecting method calls to the log API
        '''
        def __init__(self, callCollector):
            '''
            Constructor

            @param  callCollector [in] (list) List that will be appended with the call parameters
            '''
            Logger.__init__(self)
            LeveledLoggerTestCase.CollectorMixin.__init__(self, callCollector = callCollector)

            self.stub('open')
            self.stub('close')
            self.stub('logTitle1')
            self.stub('logTitle2')
            self.stub('logTitle3')
            self.stub('logError')
            self.stub('logTrace')
            self.stub('logDebug')
            self.stub('log')
            self.stub('logRaw')
            self.stub('logInfo')
            self.stub('logSeparator')
            self.stub('addPerformanceData')
        # end def __init__
    # end class MockLogger

    @classmethod
    def _createInstance(cls, level = None):
        '''
        Creates an instance of the context debugger.

        @option level [in] (int) Logging Level

        @return a new instance of the context debugger, using a dummy back-end
        '''
        callCollector = []
        logger = cls.MockLogger(callCollector)

        if (level is None):
            level = cls.RefClass.QUIET
        # end if

        return cls.RefClass(logger, level), callCollector
    # end def _createInstance

    METHODS_PARAMETERS = (('open',          None,           None),
                          ('close',         None,           None),
                          ('logTitle1',     ('message',),   RefClass.QUIET),
                          ('logTitle2',     ('message',),   RefClass.QUIET),
                          ('logTitle3',     ('message',),   RefClass.QUIET),
                          ('logError',      ('message',),   RefClass.QUIET),
                          ('logTrace',      ('message',),   RefClass.NORMAL),
                          ('logSeparator',  ('message',),   RefClass.QUIET),
                          ('logDebug',      ('message',),   RefClass.NORMAL),
                          ('log',           (1, 'message'), None),
                          ('logRaw',        ('message',),   RefClass.NORMAL),
                          ('logInfo',       ('message',),   RefClass.NORMAL),
                          )

    def testMethods(self):
        '''
        Tests methods
        '''
        instance, callCollector = self._createInstance()

        for methodName, parameters, verbosity in self.METHODS_PARAMETERS:
            del callCollector[:]
            if (parameters is None):
                getattr(instance, methodName)()
            else:
                getattr(instance, methodName)(*parameters)
            # end if

            parameters = tuple() if parameters is None else parameters
            if (   (verbosity is None)
                or (   (instance._level is None)                                                                        # pylint:disable=W0212
                    or (instance._level > verbosity))):                                                                 # pylint:disable=W0212
                self.assertTrue(('%s' % methodName, parameters, {}) in callCollector,
                                '%s not called on back-end' % methodName)

            else:
                self.assertEqual([],
                                 callCollector,
                                 'Should not be called on call-back')

            # end if

        # end for

    # end def testMethods

# end class LeveledLoggerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
