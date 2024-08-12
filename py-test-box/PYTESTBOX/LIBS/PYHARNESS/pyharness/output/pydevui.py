#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.output.pydevui

@brief  PyDev-compatible output

This module contains the listeners that output the test progress to stderr,
in PyDev-parseable format

@author christophe.roquebert

@date   2018/03/29
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core                      import TestCase
from pyharness.core                      import TestListener
from pyharness.output.common             import FileTestListenerMixin
from sys                                import stderr
from threading                          import RLock

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class PyDevTestListener(TestListener, FileTestListenerMixin):
    '''
    A test result class that logs the path to a Log file to stderr, on a
    PyDev-compatible format
    '''

    FORMAT = '\nNew log file:\n  File: "%s", line 1\n'
    FILE_FORMAT = '%s.log'
    RELATIVE_PATH = 'log'

    SYNCHRONIZATION_LOCK = RLock()

    _stderr = stderr

    def startTest(self, test):
        '''
        @copydoc pyharness.core.TestListener.startTest
        '''
        if (isinstance(test, TestCase)):
            testId = test.id()
            with self.SYNCHRONIZATION_LOCK:
                self._stderr.write(self.FORMAT % self._getOutputFilePath(testId))
            # end with
        # end if
    # end def startTest
# end class PyDevTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
