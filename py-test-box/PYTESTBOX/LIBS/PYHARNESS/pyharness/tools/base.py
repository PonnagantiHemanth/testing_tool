#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
# pylint:disable=W8008
"""
@package pyharness.tools.base

@brief  Base implementation of a program that makes use of the FEATURES

@author christophe.roquebert

@date   2018/10/26
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from argparse import ArgumentParser
from os.path import abspath
from os.path import join
from os.path import normpath
from os.path import sep
from pyharness.arguments import KeywordArguments
from pyharness.context import ContextLoader
from pyharness.core import _LEVEL_DEBUG
from pyharness.core import _LEVEL_ERROR
from pyharness.core import _LEVEL_INFO
from pyharness.core import _LEVEL_RAW
from pyharness.core import _LEVEL_SEPARATOR
from pyharness.core import _LEVEL_TITLE1
from pyharness.core import _LEVEL_TITLE2
from pyharness.core import _LEVEL_TITLE3
from pyharness.core import _LEVEL_TRACE
from pyharness.output.vblogui import VBLogFormatter
from pylibrary.tools.logger import CompositeLogger
from pylibrary.tools.logger import EmptyLogger
from pylibrary.tools.logger import Logger
from pylibrary.tools.logger import LoggerProvider
from time import localtime
from time import strftime
from traceback import format_exception
import sys


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def update_path():
    """
    Updates the system path.
    """
    # Perform a magic trick on the path
    for argv0 in [sys.argv[0], __file__]:
        argv0 = abspath(argv0)
        marker = normpath(sep + 'PYTESTBOX' + sep)
        if marker in argv0:
            root = argv0[:argv0.index(marker)]
            break
        # end if
    else:
        return
    # end for

    # Add PySetup to the pythonpath
    try:
        import pysetup
        # dummy usage of pysetup
        type(pysetup)
    except ImportError:
        sys.path.insert(0, join(root, 'LIBS', 'PYSETUP', 'PYTHON'))
    # end try

    # If a root testrunner cannot be imported, add TESTSUITES to the path
    try:
        import features
        # dummy usage of features
        type(features)
    except ImportError:
        from pysetup import TESTS_PATH  # pylint:disable=E0611

        source_path = abspath(join(TESTS_PATH, 'TESTSUITES'))
        sys.path.insert(0, source_path)
    # end try
# end def update_path


update_path()


class StreamLogger(Logger):
    """
    A base logger that redirects its logging methods to log
    """

    def __init__(self, stream, need_new_line=False, needs_close=False):
        """
        Constructor

        @param  stream      [in] (stream) The output stream
        @option need_new_line [in] (bool) Whether a newline should be inserted for each log action.
        @option needs_close  [in] (bool) Whether the stream is closed on exit
        """
        super(StreamLogger, self).__init__()

        self._stream = stream
        self._newLine = '\n' if need_new_line else ''
        self._close = needs_close
    # end def __init__

    def close(self):
        """
        Closes the stream
        """
        super(StreamLogger, self).close()

        if self._close:
            self._stream.close()
        # end if
    # end def close

    def log(self, log_level, msg, *args, **kwargs):  # pylint:disable=R0201
        """
        @copydoc pylibrary.tools.logger.Logger.log
        """
        if len(args):
            message = msg % args
        elif len(kwargs):
            message = msg % kwargs
        else:
            message = msg
        # end if

        self._stream.write(self._newLine + VBLogFormatter.format(log_level, message))
    # end def log

    def logError(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logError
        """
        self.log(_LEVEL_ERROR, msg, *args, **kwargs)
    # end def logError

    def logTitle1(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle1
        """
        self.log(_LEVEL_TITLE1, msg, *args, **kwargs)
    # end def logTitle1

    def logTitle2(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle2
        """
        self.log(_LEVEL_TITLE2, msg, *args, **kwargs)
    # end def logTitle2

    def logTitle3(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle3
        """
        self.log(_LEVEL_TITLE3, msg, *args, **kwargs)
    # end def logTitle3

    def logSeparator(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logSeparator
        """
        self.log(_LEVEL_SEPARATOR, msg, *args, **kwargs)
    # end def logSeparator

    def logTrace(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTrace
        """
        self.log(_LEVEL_TRACE, msg, *args, **kwargs)
    # end def logTrace

    def logDebug(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logDebug
        """
        self.log(_LEVEL_DEBUG, msg, *args, **kwargs)
    # end def logDebug

    def logRaw(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logRaw
        """
        self.log(_LEVEL_RAW, msg, *args, **kwargs)
    # end def logRaw

    def logInfo(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logRaw
        """
        self.log(_LEVEL_INFO, msg, *args, **kwargs)
    # end def logInfo
# end class StreamLogger


class LeveledLogger(Logger):  # pylint:disable=W0223
    """
    A logger that filters the input based on the level
    """

    QUIET = 0
    NORMAL = 1
    VERBOSE = 2

    def __init__(self, logger, level):
        """
        Constructor

        @param  logger [in] (Logger) The final logger to use
        @param  level  [in] (int) The logger level
        """
        super(LeveledLogger, self).__init__()

        self._logger = logger
        self._level = level
    # end def __init__

    def __proxy(name, level=None):  # @NoSelf #pylint:disable=E0213
        """
        Creates a proxy for a given method, filtering based in the level

        @param  name  [in] (str) Name of the method to delegate to
        @option level [in] (int) the level to filter

        @return A delegate method
        """
        def delegate(self, *args, **kwargs):
            """
            Delegate method for checking for level.

            @param  args   [in] (tuple) Arguments
            @param  kwargs [in] (dict) Keyword arguments
            """
            if (self._level is None) or (level is None) or (self._level > level):  # pylint:disable=W0212
                target = getattr(self._logger, name)  # pylint:disable=W0212
                target(*args, **kwargs)
            # end if
        # end def delegate

        return delegate
    # end def __proxy

    def log(self, log_level, msg, *args, **kwargs):  # pylint:disable=R0201
        """
        @copydoc pylibrary.tools.logger.Logger.log
        """
        self._logger.log(log_level, msg, *args, **kwargs)
    # end def log

    open = __proxy('open')  # @ReservedAssignment

    close = __proxy('close')

    logError = __proxy('logError', QUIET)

    logTitle1 = __proxy('logTitle1', QUIET)

    logTitle2 = __proxy('logTitle2', QUIET)

    logTitle3 = __proxy('logTitle3', QUIET)

    logSeparator = __proxy('logSeparator', QUIET)

    logTrace = __proxy('logTrace', NORMAL)

    logDebug = __proxy('logDebug', NORMAL)

    logRaw = __proxy('logRaw', NORMAL)

    logInfo = __proxy('logInfo', NORMAL)
# end class LeveledLogger


class Provider(Logger, LoggerProvider):
    """
    A wrapper class that implements getDevice, logger methods, etc
    """

    def __init__(self, context, logger=None):
        """
        Constructor

        @param  context [in] (Context) The context to wrap
        @option logger  [in] (Logger) The current logger
        """
        super(Provider, self).__init__()

        self._context = context
        self._devices = {}
        self._logger = logger if logger is not None else EmptyLogger()
    # end def __init__

    def getLogger(self):
        """
        @copydoc pylibrary.tools.logger.LoggerProvider.getLogger
        """
        return self._logger
    # end def getLogger

    def getContext(self):
        """
        Obtains the context

        @return The context
        """
        return self._context
    # end def getContext

    def getDevice(self, index_or_predicate=0, *args, **kwargs):
        """
        Proxy method for the getDevice API

        @option index_or_predicate [in] (int,callable) The TestCases on which to obtain the device
        @option args             [in] (tuple) The arguments
        @option kwargs           [in] (dict) The keyword arguments

        @return The result of Context.getDevice
        """
        pass
    # end def getDevice

    def getFeatures(self, *args, **kwargs):
        """
        Proxy method for the getFeatures API

        @option args   [in] (tuple) The arguments
        @option kwargs [in] (dict)  The keyword arguments

        @return The result of Context.getDevice
        """
        return self._context.getFeatures(*args, **kwargs)
    # end def getFeatures

    def log(self, log_level, msg, *args, **kwargs):  # pylint:disable=R0201
        """
        @copydoc pylibrary.tools.logger.Logger.log
        """
        self._logger.log(log_level, msg, *args, **kwargs)
    # end def log

    def logError(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logError
        """
        self._logger.logError(msg, *args, **kwargs)
    # end def logError

    def logTitle1(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle1
        """
        self._logger.logTitle1(msg, *args, **kwargs)
    # end def logTitle1

    def logTitle2(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle2
        """
        self._logger.logTitle2(msg, *args, **kwargs)
        # end if
    # end def logTitle2

    def logTitle3(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTitle3
        """
        self._logger.logTitle3(msg, *args, **kwargs)
    # end def logTitle3

    def logSeparator(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logSeparator
        """
        self._logger.logSeparator(msg, *args, **kwargs)
    # end def logSeparator

    def logTrace(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logTrace
        """
        self._logger.logTrace(msg, *args, **kwargs)
    # end def logTrace

    def logDebug(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logDebug
        """
        self._logger.logDebug(msg, *args, **kwargs)
    # end def logDebug

    def logRaw(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logRaw
        """
        self._logger.logRaw(msg, *args, **kwargs)
    # end def logRaw

    def logInfo(self, msg, *args, **kwargs):  # pylint:disable=W0613
        """
        @copydoc pylibrary.tools.logger.Logger.logRaw
        """
        self._logger.logInfo(msg, *args, **kwargs)
    # end def logInfo

    def close(self):
        """
        Close Provider at the end of tools
        """
        self._logger.close()
    # end def close
# end class Provider


class Main(object):
    """
    A program that:
    - Works on the current configuration
    -
    """
    # Overridden by all tools
    DEFAULT_ARGUMENTS_OVERRIDE = {}

    VERSION = None

    def __init__(self, argv, stdout=None, stderr=None):
        """
        Constructor and main program entry point

        @param  argv   [in] (tuple)  The program arguments
        @option stdout [in] (stream) The standard output stream
        @option stderr [in] (stream) The standard error stream
        """
        assert self.VERSION is not None, ValueError('A tool MUST define a VERSION')

        # Tool log is saved in a file
        self._save_log_file = None
        # Tool log is displayed in console or not
        self._console_display = False
        # Display Level
        self._loglevel = LeveledLogger.NORMAL
        # Device, logger provider
        self._provider = None
        self._stdout = stdout
        self._stderr = stderr

        self._kw_args = self.parse_args(argv)

        # Specify the root path
        root_paths = [self._kw_args[KeywordArguments.KEY_ROOT]]
        root_paths.extend(self._kw_args[KeywordArguments.KEY_EXTENDEDROOTS])

        # Load the context
        context_loader = ContextLoader()
        self._config = context_loader.loadConfig(rootPaths=root_paths,
                                                 overrides=self._kw_args[KeywordArguments.KEY_OVERRIDES])

        context = context_loader.createContext(self._config)
        self._context = context

        loggers = []
        if self._console_display:
            loggers.append(StreamLogger(stdout))
        # end if

        if self._save_log_file:
            with open(self._save_log_file, 'w+') as logFile:
                loggers.append(StreamLogger(logFile))
            # end with
        # end if

        logger = LeveledLogger(CompositeLogger(loggers), self._loglevel)

        self._provider = Provider(context, logger=logger)
    # end def __init__

    def _logStart(self):
        """
        Logs the log header
        """
        logger = self._provider.getLogger()

        # Create Log File Header
        logger.logSeparator('')

        # Log the tool description
        logger.logTrace(self.__doc__)

        # Log the test date and time
        time_string = strftime("[DateTime] %Y-%m-%d %H:%M:%S\n", localtime())
        logger.logTrace(time_string)

        logger.logTrace('')

        # Log the test configuration
        context = self._provider.getContext()
        config = context.getConfig()
        product = config.get(ContextLoader.SECTION_PRODUCT, ContextLoader.OPTION_VALUE)
        variant = config.get(ContextLoader.SECTION_VARIANT, ContextLoader.OPTION_VALUE)
        logger.logTrace(f"[Settings]\n - Product  {product}\n - Variant  {variant}\n")

        logger.logTrace(' ')
        logger.logSeparator('')
    # end def _logStart

    def run(self):
        """
        Perform the program's action and manage exception

        @return The status of the action: 0 if successful, 1 in cas of exception.
        """
        # Perform action
        # --------------
        status = 0
        try:
            self._logStart()  # pylint:disable=C0321
            self.do_action()
        except Exception:  # pylint:disable=W0703
            last_exception = self.__exc_info()

            # data is an __excinfo
            tracelist = format_exception(*last_exception)
            self._provider.logError("\n".join(tracelist))
            status = 1
        finally:
            # Close correctly the provider
            self._provider.close()
        # end try

        return status
    # end def run

    def do_action(self):
        """
        Perform the program's action.

        This is the main worker method of the derived tools, and it MUST
        be implemented by the derived classes
        """
        pass
    # end def do_action

    @staticmethod
    def __exc_info():
        """
        Return a version of sys.exc_info() with the traceback frame minimized;

        Usually the top level of the traceback frame is not needed, as it only
        contains internal, pyharness-specific information.

        @return Tuple
        """
        exc_type, exc_value, tb = sys.exc_info()
        tup = (exc_type, exc_value, tb,)
        # tracebacks look different in Jython
        if sys.platform[:4] == 'java':
            return tup
        # end if
        new_tb = tb.tb_next
        if new_tb is None:
            return tup
        # end if
        tup = (exc_type, exc_value, new_tb,)
        return tup
    # end def __exc_info

    def get_parser(self):
        """
        Obtains the argument parser, with some options already initialized

        @return ArgumentParser The argument parser, in charge of parsing the command line arguments.
        """
        parser = ArgumentParser()
        parser.add_argument('--version', action='version', version=self.VERSION)
        parser.add_argument('-v', '--verbose', dest='verbose', help='maximal output', default=False,
                            action='store_true')
        parser.add_argument('-m', '--medium', dest='medium', help='medium output', default=False,
                            action='store_true')
        parser.add_argument('-q', '--quiet', dest='quiet', help='minimal output', default=False,
                            action='store_true')
        parser.add_argument('-c', '--console', dest='console', help='output to console formats', default=False,
                            action='store_true')
        parser.add_argument('-r', '--root', dest='root', help='use ROOT as the validation directory', default=None,
                            metavar='ROOT')
        parser.add_argument('-P', '--product', dest='product', help='use the specified PRODUCT', default=None,
                            metavar='PRODUCT')
        parser.add_argument('-V', '--variant', dest='variant', help='use the specified VARIANT', default=None,
                            metavar='VARIANT')
        parser.add_argument('-T', '--target', dest='target', help='use the specified TARGET', default=None,
                            metavar='TARGET')
        parser.add_argument('-M', '--mode', dest='mode', help='use the specified MODE', default=None,
                            metavar='MODE')
        parser.add_argument('-L', '--logfile', dest='logFile', help='log output to LOGFILE', default=None,
                            metavar='LOGFILE')

        return parser
    # end def get_parser

    def parse_args(self, argv, kw_args=None):
        """
        Parses the program arguments

        @param  argv    [in] (tuple) The arguments passed in the command line.
        @param kw_args  [in] (dict) A collecting dictionary for the keyword arguments.
                           This should be a COPY for the default keyword arguments.
        @return A dict of keyword arguments, passed to the inner structures.
        """
        parser = self.get_parser()
        args = parser.parse_args(argv[1:])

        # Obtain a copy of the default Keyword arguments
        # The KeywordArguments are a way to pass arguments through all the
        # program layers, without actually adding parameters each time a new
        # argument is needed.
        if kw_args is None:
            kw_args = KeywordArguments.DEFAULT_ARGUMENTS.copy()
            kw_args.update(self.DEFAULT_ARGUMENTS_OVERRIDE)
        # end if

        # Iterate over the args.
        if args.quiet:
            self._loglevel = LeveledLogger.QUIET
        elif args.medium:
            self._loglevel = LeveledLogger.NORMAL
        elif args.verbose:
            self._loglevel = LeveledLogger.VERBOSE
        # end if

        if args.root is not None:
            kw_args[KeywordArguments.KEY_ROOT] = abspath(args.root.strip())
        # end if

        if args.product is not None:
            override = f"{ContextLoader.SECTION_PRODUCT}.{ContextLoader.OPTION_VALUE}={args.product}"
            kw_args[KeywordArguments.KEY_OVERRIDES].append(override)
        # end if

        if args.variant is not None:
            override = f"{ContextLoader.SECTION_VARIANT}.{ContextLoader.OPTION_VALUE}={args.variant}"
            kw_args[KeywordArguments.KEY_OVERRIDES].append(override)
        # end if

        if args.target is not None:
            override = f"{ContextLoader.SECTION_TARGET}.{ContextLoader.OPTION_VALUE}={args.target}"
            kw_args[KeywordArguments.KEY_OVERRIDES].append(override)
        # end if

        if args.mode is not None:
            override = f"{ContextLoader.SECTION_MODE}.{ContextLoader.OPTION_VALUE}={args.mode}"
            kw_args[KeywordArguments.KEY_OVERRIDES].append(override)
        # end if

        if args.logFile is not None:
            self._save_log_file = args.logFile
        # end if

        # Change the root dir to the absolute directory
        kw_args[KeywordArguments.KEY_ROOT] = abspath(kw_args[KeywordArguments.KEY_ROOT])

        return kw_args
    # end def parse_args
# end class Main


if __name__ == '__main__':
    Main(sys.argv, sys.stdout, sys.stderr)
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
