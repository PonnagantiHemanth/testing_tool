#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyharness.output.metricsui
:brief: Metrics file TestListener
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/08/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import shutil
from os import F_OK
from os import access
from os import makedirs
from os import stat
from os.path import exists

from pyharness.core import TestSuite
from pyharness.core import _LEVEL_ERROR
from pyharness.core import _LEVEL_TITLE1
from pyharness.core import _MASK_ALWAYS
from pyharness.output.logui import LogTestListener
from pyharness.output.vblogui import VBLogFormatter


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MetricsTestListener(LogTestListener):
    """
    A test listener class that can print formatted text results to a file.

    The file format follows the format defined by ValidVB.
    """

    RELATIVE_PATH = 'metrics'
    FILE_FORMAT = '%s.log'
    METRICS_FILE_NAME = 'metrics'
    MAX_FILE_SIZE_BYTE = 512 * 1024
    AVAILABLE_METRICS_LENGTH = 3

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``pyharness.core.LogTestListener.__init__``
        super().__init__(descriptions, verbosity, outputdir, args)
        self.metrics_str = []
    # end def __init__

    def log(self, test, level, msg, *args, **kwargs):
        # See ``pyharness.core.LogTestListener.log``
        if level in [_LEVEL_TITLE1 + _MASK_ALWAYS, _LEVEL_ERROR + _MASK_ALWAYS]:
            # Log the test description and configuration
            self.metrics_str.append(VBLogFormatter.format(level, msg))
        # end if
    # end def log

    def startRun(self, context, resumed): # pylint:disable=W0613
        # See ``pyharness.core.LogTestListener.startRun``
        super().startRun(context, resumed)

        log_path = self._getOutputFilePath(self.METRICS_FILE_NAME)
        # Remove all records if the size of metrics file exceeds the up limit.
        if exists(log_path) and stat(log_path).st_size > self.MAX_FILE_SIZE_BYTE:
            # Move records to the backup file
            dst_dir = self._getOutputFilePath(self.METRICS_FILE_NAME + '_backup')
            shutil.copy(log_path, dst_dir)
            # Remove records in the metrics log file
            log_file = open(log_path, "w+")
            log_file.close()
        # end if
    # end def startRun

    def startTest(self, test):
        # See ``pyharness.output.vblogui.BaseLogTestListener.startTest``
        # create a logger
        test_id = test.id()

        # create a stream handler, that will dump the logs in a string
        with self.SYNCHRONIZATION_LOCK:
            log_dir = self._resultDirPath()
            if not access(log_dir, F_OK):
                makedirs(log_dir)
            # end if
        # end with

        log_path = self._getOutputFilePath(self.METRICS_FILE_NAME)
        # Initialize the header
        log_file = open(log_path, "a+")
        self.logFiles[test_id] = log_file

        # Initialize the header
        text = f"# [TestName]  {test_id}"
        hash_line = VBLogFormatter.getSeparator(len(text))
        self.metrics_str.append(f"{hash_line}{text}\n{hash_line}")
    # end def startTest

    def addPerformanceData(self, test, key, value, unit=None):
        # See ``pyharness.core.TestListener.addPerformanceData``
        self.metrics_str.append(f'{key} = {value}')
    # end def addPerformanceData

    def stopTest(self, test):
        # See ``pyharness.output.vblogui.BaseLogTestListener.stopTest``
        super(LogTestListener, self).stopTest(test)

        if not isinstance(test, TestSuite):
            test_id = test.id()

            # Commit the metrics to file
            len_metrics = len(self.metrics_str)
            if len_metrics >= self.AVAILABLE_METRICS_LENGTH:
                log_file = self.logFiles[test_id]
                for index, msg in enumerate(self.metrics_str):
                    if len(msg) and (msg[-1] != '\n'):
                        if index + 1 < len_metrics:
                            if len(self.metrics_str[index + 1]) and (self.metrics_str[index + 1][0] != '\n'):
                                msg += '\n'
                            # end if
                        else:
                            msg += '\n'
                        # end if
                    # end if
                    log_file.write(msg)
                # end for
                log_file.write('\n')
            # end if
            self.metrics_str.clear()

            # Commit the log file to disk
            self._destroy_and_save_logger(test)
        # end if
    # end def stopTest
# end class MetricsTestListener
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
