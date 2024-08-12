#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.output.logui
:brief: LOG file TestListener
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/09
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os import F_OK
from os import access
from os import listdir
from os import makedirs
from os import remove
from os.path import join
from threading import RLock

from pyharness.arguments import KeywordArguments
from pyharness.core import TestSuite
from pyharness.core import _LEVEL_TRACE
from pyharness.output.common import FileTestListenerMixin
from pyharness.output.vblogui import BaseVBLogTestListener
from pyharness.output.vblogui import VBLogFormatter


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LogTestListener(BaseVBLogTestListener, FileTestListenerMixin):
    """
    A test listener class that can print formatted text results to a file.

    The file format follows the format defined by ValidVB.
    """

    RELATIVE_PATH = 'log'
    FILE_FORMAT = '%s.log'
    SYNCHRONIZATION_LOCK = RLock()

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``pyharness.core.TestListener.__init__``
        # Keep at least the trace verbosity level for the .log file to enable the test failures analysis
        verbosity = _LEVEL_TRACE if verbosity > _LEVEL_TRACE else verbosity
        super(LogTestListener, self).__init__(descriptions, verbosity, outputdir, args)

        self.logFiles = {}
        self._testCasesDir = None
    # end def __init__

    def __createLogger(self, test):
        """
        Creates a logger for the test.

        The logger dumps the log data to a log file, which is
        deleted upon test success

        @param  test [in] (TestCase) The test to log.
        """
        # create a logger
        test_id = test.id()

        # create a stream handler, that will dump the logs in a string
        with self.SYNCHRONIZATION_LOCK:
            log_dir = self._resultDirPath()
            if not access(log_dir, F_OK):
                makedirs(log_dir)
            # end if
        # end with

        log_path = self._getOutputFilePath(test_id)

        # Initialize the header
        log_file = open(log_path, "w+")
        text = f"# [TestName]  {test_id}"
        hash_line = VBLogFormatter.getSeparator(len(text))
        log_file.write(f"{hash_line}{text}\n{hash_line}")
        log_file.flush()
        self.logFiles[test_id] = log_file
    # end def __createLogger

    def _destroy_and_save_logger(self, test):
        """
        Destroys (detach) a logger for the test.

        @note   This only closes the file, and does not delete it.

        @param  test [in] (TestCase) The test to log
        """
        # remove the logger handler
        test_id = test.id()
        log_file = self.logFiles[test_id]
        log_file.close()

        del self.logFiles[test_id]
    # end def _destroy_and_save_logger

    def startRun(self, context, resumed): # pylint:disable=W0613
        # See ``pyharness.core.TestListener.startRun``
        # Empties if needed all log files
        if (not resumed) and (self.args[KeywordArguments.KEY_ERASELOGS]):

            output_dir = join(self.outputdir, self.RELATIVE_PATH)
            if access(output_dir, F_OK):
                import re

                file_pattern = re.compile('^' + (self.FILE_FORMAT % '.*') + '$')
                # Erase _all_ tests in the directory.
                for filename in listdir(output_dir):
                    if file_pattern.match(filename):
                        remove(join(output_dir, filename))
                    # end if
                # end for
            # end if
        # end if
    # end def startRun

    def resetTest(self, test, context): # pylint:disable=W0613
        # See ``pyharness.core.TestListener.resetTest``
        test_id = test.id()
        log_path = self._getOutputFilePath(test_id)
        if access(log_path, F_OK):
            remove(log_path)
        # end if
    # end def resetTest

    def startTest(self, test):
        # See ``pyharness.output.vblogui.BaseLogTestListener.startTest``
        if not isinstance(test, TestSuite):
            self.__createLogger(test)
        # end if
    # end def startTest

    def stopTest(self, test):
        # See ``pyharness.output.vblogui.BaseLogTestListener.stopTest``
        super(LogTestListener, self).stopTest(test)

        if not isinstance(test, TestSuite):

            test_id = test.id()

            # Commit the log file to disk
            self._destroy_and_save_logger(test)

            # Discard the log file, if needed and no warning occurs
            if ((test_id not in self.nonsuccesses)
                    and (not self.args[KeywordArguments.KEY_KEEPLOGS])
                    and not test.warning_occurred):
                log_path = self._getOutputFilePath(test_id)
                try:
                    remove(log_path)
                except Exception:  # pylint:disable=W0703
                    # Ticket #338: This ignores any error while removing the path.
                    # The drawback is that the file is NOT removed, but this
                    # should not happen too often (if another process has already
                    # opened the file.)
                    pass
                # end try
            # end if

            if test_id in self.nonsuccesses:
                del self.nonsuccesses[test_id]
            # end if
        # end if
    # end def stopTest

    def log(self, test, level, msg, *args, **kwargs):
        # See ``pyharness.core.TestListener.log``
        if self.acceptLog(level):
            test_id = test.id()

            if test_id in self.logFiles:
                log_file = self.logFiles[test_id]
                if len(args) > 0:
                    message = msg % args
                elif len(kwargs) > 0:
                    message = msg % kwargs
                else:
                    message = msg
                # end if

                msg = VBLogFormatter.format(level, message)
                log_file.write(msg)

                if len(msg) and (msg[-1] != '\n'):
                    log_file.write('\n')
                # end if
            # end if
        # end if
    # end def log

    def getResultDirPath(self):
        # See ``pyharness.output.common.FileTestListenerMixin._resultDirPath``
        return self._resultDirPath()
    # end def getResultDirPath
# end class LogTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
