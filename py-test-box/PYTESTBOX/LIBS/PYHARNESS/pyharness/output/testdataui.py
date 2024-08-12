#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyharness.output.testdatatui
:brief: Test data file TestListener
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/07/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from os import remove

from pyharness.core import TestSuite
from pyharness.core import _LEVEL_TITLE1
from pyharness.core import _MASK_ALWAYS
from pyharness.output.logui import LogTestListener


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TestDataTestListener(LogTestListener):
    """
    A test listener class that can print formatted text results to a file.

    The file format follows the format defined by ValidVB.
    """

    RELATIVE_PATH = 'test_data'
    FILE_FORMAT = '%s.log'

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``pyharness.core.LogTestListener.__init__``
        super().__init__(descriptions, verbosity, outputdir, args)
        # List of files which will not be wiped out when the test is stopped even if there is no errors or failures
        # The call to the "add_test_data" method will update this list
        self.keep_files = []
    # end def __init__

    def log(self, test, level, msg, *args, **kwargs):
        # See ``pyharness.core.LogTestListener.log``
        if level == _LEVEL_TITLE1 + _MASK_ALWAYS:
            # Log the test description and configuration
            super().log(test, level, msg, *args, **kwargs)
        # end if
    # end def log

    def add_test_data(self, test, data):
        # See ``pyharness.core.TestListener.add_test_data``
        test_id = test.id()
        log_file = self.logFiles[test_id]
        msg = f' {data}\n' if data[-1] != '\n' else f' {data}'

        if test_id in self.logFiles:
            log_file.write(msg)
            self.keep_files.append(test_id)
        # end if
    # end def add_test_data

    def stopTest(self, test):
        # See ``pyharness.output.vblogui.BaseLogTestListener.stopTest``
        super(LogTestListener, self).stopTest(test)

        if not isinstance(test, TestSuite):
            test_id = test.id()

            # Commit the log file to disk
            self._destroy_and_save_logger(test)

            # Discard the log file, if needed and no warning occurs
            if test_id not in self.keep_files:
                log_path = self._getOutputFilePath(test_id)
                # noinspection PyBroadException
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
# end class TestDataTestListener
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
