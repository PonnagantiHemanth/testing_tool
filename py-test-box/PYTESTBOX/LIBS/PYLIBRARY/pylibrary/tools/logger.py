#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.logging

@brief  Interface definition of a Logger

@author christophe.roquebert

@date   2018/10/23
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import logging
# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LoggerProvider(object):
    '''
    Interface implemented by objects able of provide an instance of a Logger
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor

        @param  args   [in] (tuple) arguments
        @param  kwargs [in] (dict)  keyword arguments
        '''
        super(LoggerProvider, self).__init__(*args, **kwargs)
    # end def __init__

    def getLogger(self):
        '''
        Obtains an instance of a logger.

        @return Logger A logger instance
        '''
        raise NotImplementedError
    # end def getLogger
# end class LoggerProvider

class Logger(object):
    '''
    Interface definition of a logger.

    A logger is an object able to log (!!!) some data to a persistent storage.
    '''

    def __init__(self, *args, **kwargs):
        '''
        Constructor

        @param  args   [in] (tuple) arguments
        @param  kwargs [in] (dict)  keyword arguments
        '''
        pass
    # end def __init__

    def open(self):                                                                                                     #@ReservedAssignment
        '''
        Opens the logger, performing necessary operations (open file, open connection...)
        '''
        pass
    # end def open

    def close(self):
        '''
        Close the logger, performing necessary operations (open file, open connection...)
        '''
        pass
    # end def close

    def logError(self, msg, *args, **kwargs):
        '''
        Error log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logError

    def logTitle1(self, msg, *args, **kwargs):
        '''
        Title 1 log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logTitle1

    def logTitle2(self, msg, *args, **kwargs):
        '''
        Title 2 log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logTitle2

    def logTitle3(self, msg, *args, **kwargs):
        '''
        Title 3 log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logTitle3

    def logSeparator(self, msg, *args, **kwargs):
        '''
        Separator log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logSeparator

    def logTrace(self, msg, *args, **kwargs):
        '''
        Trace log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logTrace

    def logDebug(self, msg, *args, **kwargs):
        '''
        Debug log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logDebug

    def logRaw(self, msg, *args, **kwargs):
        '''
        Raw log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logRaw

    def logInfo(self, msg, *args, **kwargs):
        '''
        Information log writing

        @param  msg    [in] (str)   Message to log
        @option args   [in] (tuple) List of arguments
        @option kwargs [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def logInfo

    def log(self, logLevel, msg, *args, **kwargs):
        '''
        Parameterized log writing

        @param  logLevel [in] (int)   Log level, as an int.
                                      This is implementation-specific.
        @param  msg      [in] (str)   Message to log
        @option args     [in] (tuple) List of arguments
        @option kwargs   [in] (dict)  Keyword arguments
        '''
        raise NotImplementedError
    # end def log

# end class Logger

class EmptyLogger(Logger):
    '''
    An empty logger, that implements all Logger methods but does nothing.
    '''
    def logError(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logError
        '''
        pass
    # end def logError

    def logTitle1(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logTitle1
        '''
        pass
    # end def logTitle1

    def logTitle2(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logTitle2
        '''
        pass
    # end def logTitle2

    def logTitle3(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logTitle3
        '''
        pass
    # end def logTitle3

    def logSeparator(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logSeparator
        '''
        pass
    # end def logSeparator

    def logTrace(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logTrace
        '''
        pass
    # end def logTrace

    def logDebug(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logDebug
        '''
        pass
    # end def logDebug

    def logRaw(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logRaw
        '''
        pass
    # end def logRaw

    def logInfo(self, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.logInfo
        '''
        pass
    # end def logInfo

    def log(self, logLevel, msg, *args, **kwargs):
        '''
        @copydoc pylibrary.tools.logging.Logger.log
        '''
        pass
    # end def log
# end class EmptyLogger

class CompositeLogger(Logger):                                                                                          #pylint:disable=W0223
    '''
    A Logger that dispatches its inputs to child loggers
    '''
    def __init__(self, loggers):
        '''
        Constructor

        @param  loggers [in] (list) The loggers to delegate the actions to
        '''
        super(CompositeLogger, self).__init__()

        self._loggers = loggers
    # end def __init__

    def __proxy(name):                                                                                                  #@NoSelf #pylint:disable=E0213
        '''
        Creates a delegating function that dispatches the calls to child loggers

        @param  name [in] (str) Name of the proxied method
        @return A delegate method
        '''
        def delegate(self, *args, **kwargs):
            '''
            Delegates a call to child loggers

            @option args   [in] (tuple) arguments
            @option kwargs [in] (dict)  keyword arguments
            '''
            for logger in self._loggers:                                                                               #pylint:disable=W0212
                try:
                    childMethod = getattr(logger, name)
                    childMethod(*args, **kwargs)
                except Exception:                                                                                       #pylint:disable=W0703
                    pass
                # end try
            # end for
        # end def delegate

        return delegate
    # end def __proxy

    open         = __proxy('open')                                                                                      #@ReservedAssignment

    close        = __proxy('close')

    logError     = __proxy('logError')

    logTitle1    = __proxy('logTitle1')

    logTitle2    = __proxy('logTitle2')

    logTitle3    = __proxy('logTitle3')

    logSeparator = __proxy('logSeparator')

    logTrace     = __proxy('logTrace')

    logDebug     = __proxy('logDebug')

    logRaw       = __proxy('logRaw')

    logInfo      = __proxy('logInfo')

    log          = __proxy('log')
# end class CompositeLogger

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
