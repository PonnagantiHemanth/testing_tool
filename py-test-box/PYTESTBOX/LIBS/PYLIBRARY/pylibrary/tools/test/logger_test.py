#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.logging

@brief  Logging testing module

@author christophe Roquebert

@date   2018/06/08
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.logger           import CompositeLogger
from pylibrary.tools.logger           import EmptyLogger
from pylibrary.tools.logger           import Logger
from pylibrary.tools.logger           import LoggerProvider
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LoggerProviderTestCase(TestCase):
    '''
    LoggerProvider testing class
    '''
    RefClass = LoggerProvider

    @classmethod
    def _createInstance(cls):
        '''
        Create an instance of referenced class

        @return (object) Instance of referenced class
        '''
        return cls.RefClass()
    # end def _createInstance

    def testGetLogger(self):
        '''
        Tests getLogger method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.getLogger)

    # end def testGetLogger

# end class LoggerProviderTestCase

class LoggerTestCase(TestCase):
    '''
    Logger testing class
    '''
    RefClass = Logger

    @classmethod
    def _createInstance(cls):
        '''
        Create an instance of referenced class

        @return (object) Instance of referenced class
        '''
        return cls.RefClass()
    # end def _createInstance

    def testOpen(self):
        '''
        Tests open method
        '''
        instance = self._createInstance()

        instance.open()

    # end def testOpen

    def testClose(self):
        '''
        Tests close method
        '''
        instance = self._createInstance()

        instance.close()

    # end def testClose

    def testLogError(self):
        '''
        Tests logError method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logError,
                          'message')

    # end def testLogError

    def testLogTitle1(self):
        '''
        Tests logTitle1 method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logTitle1,
                          'message')

    # end def testLogTitle1

    def testLogTitle2(self):
        '''
        Tests logTitle2 method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logTitle2,
                          'message')

    # end def testLogTitle2

    def testLogTitle3(self):
        '''
        Tests logTitle3 method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logTitle3,
                          'message')

    # end def testLogTitle3

    def testLogSeparator(self):
        '''
        Tests logSeparator method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logSeparator,
                          'message')

    # end def testLogSeparator

    def testLogTrace(self):
        '''
        Tests logTrace method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logTrace,
                          'message')

    # end def testLogTrace

    def testLogDebug(self):
        '''
        Tests logDebug method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logDebug,
                          'message')

    # end def testLogDebug

    def testLogRaw(self):
        '''
        Tests logRaw method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logRaw,
                          'message')

    # end def testLogRaw

    def testLogInfo(self):
        '''
        Tests logInfo method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.logInfo,
                          'message')

    # end def testLogInfo

    def testLog(self):
        '''
        Tests log method
        '''
        instance = self._createInstance()

        self.assertRaises(NotImplementedError,
                          instance.log,
                          1, 'message')

    # end def testLog

# end class LoggerTestCase

class EmptyLoggerTestCase(LoggerTestCase):
    '''
    EmptyLogger testing class
    '''
    RefClass = EmptyLogger

    def testLogError(self):
        '''
        Tests logError method
        '''
        instance = self._createInstance()

        instance.logError('message')

    # end def testLogError

    def testLogTitle1(self):
        '''
        Tests logTitle1 method
        '''
        instance = self._createInstance()

        instance.logTitle1('message')

    # end def testLogTitle1

    def testLogTitle2(self):
        '''
        Tests logTitle2 method
        '''
        instance = self._createInstance()

        instance.logTitle2('message')

    # end def testLogTitle2

    def testLogTitle3(self):
        '''
        Tests logTitle3 method
        '''
        instance = self._createInstance()

        instance.logTitle3('message')

    # end def testLogTitle3

    def testLogSeparator(self):
        '''
        Tests logSeparator method
        '''
        instance = self._createInstance()

        instance.logSeparator('message')

    # end def testLogSeparator

    def testLogTrace(self):
        '''
        Tests logTrace method
        '''
        instance = self._createInstance()

        instance.logTrace('message')

    # end def testLogTrace

    def testLogDebug(self):
        '''
        Tests logDebug method
        '''
        instance = self._createInstance()

        instance.logDebug('message')

    # end def testLogDebug

    def testLogRaw(self):
        '''
        Tests logRaw method
        '''
        instance = self._createInstance()

        instance.logRaw('message')

    # end def testLogRaw

    def testLogInfo(self):
        '''
        Tests logInfo method
        '''
        instance = self._createInstance()

        instance.logInfo('message')

    # end def testLogInfo

    def testLog(self):
        '''
        Tests log method
        '''
        instance = self._createInstance()

        instance.log(1, 'message')

    # end def testLog

# end class EmptyLoggerTestCase

class CompositeLoggerTestCase(TestCase):
    '''
    CompositeLogger testing class
    '''
    RefClass = CompositeLogger

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
            CompositeLoggerTestCase.CollectorMixin.__init__(self, callCollector = callCollector)

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
    def _createInstance(cls):
        '''
        Creates an instance of the context debugger.

        @return a new instance of the context debugger, using a dummy back-end
        '''
        callCollector = []
        logger1 = cls.MockLogger(callCollector)
        logger2 = cls.MockLogger(callCollector)
        return cls.RefClass((logger1, logger2)), callCollector
    # end def _createInstance

    METHODS_PARAMETERS = (('open', None),
                          ('close', None),
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

    def testMethods(self):
        '''
        Tests methods
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

    # end def testMethods

# end class CompositeLoggerTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
