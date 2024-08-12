#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyharness.output.stdoutui
:brief: stdout TestListener
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/01/21
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.core import TestSuite
from pyharness.output.vblogui import BaseVBLogTestListener
from pyharness.output.vblogui import VBLogFormatter
from sys import stdout


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class StdoutTestListener(BaseVBLogTestListener):
    """
    A test listener class that can print formatted text results to stdout

    The file format follows the format defined by ValidVB.
    """

    _stdout = stdout

    def __init__(self, descriptions, verbosity, outputdir, args):
        # See ``pyharness.core.TestListener.__init__``
        # At the lowest setting, only the test id is printed.
        # At higher settings, a complete test description is printed.

        super(StdoutTestListener, self).__init__(descriptions, verbosity, outputdir, args)
    # end def __init__

    def startTest(self, test):
        # See ``pyharness.output.vblogui.BaseVBLogTestListener.startTest``
        if not isinstance(test, TestSuite):
            text = f"# test  {test.id()}"
            hash_line = VBLogFormatter.getSeparator(len(text))
            self._stdout.write(f"{hash_line}{text}\n{hash_line}")
            self._stdout.flush()
        # end if
    # end def startTest

    def log(self, test, level, msg, *args, **kwargs):
        # See ``pyharness.core.TestListener.log``
        if self.acceptLog(level):
            if len(args) > 0:
                message = msg % args
            elif len(kwargs) > 0:
                message = msg % kwargs
            else:
                message = msg
            # end if

            msg = VBLogFormatter.format(level, message)
            self._stdout.write(msg)

            if (len(msg)) and (msg[-1] != '\n'):
                self._stdout.write('\n')
            # end if

            self._stdout.flush()
        # end if
    # end def log
# end class StdoutTestListener

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
