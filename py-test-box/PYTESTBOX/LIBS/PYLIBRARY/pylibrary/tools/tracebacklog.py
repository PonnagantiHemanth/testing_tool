#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.tools.tracebacklog
    :brief: Traceback log wrapper
    :author: Stanislas Cottard
    :date: 2020/08/06
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from sys import exc_info
from traceback import format_exc
from traceback import format_stack


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class TracebackLogWrapper:
    @staticmethod
    def get_traceback_stack():
        if exc_info()[0] is None:
            return TracebackLogWrapper.get_regular_stack()
        # end if

        return TracebackLogWrapper.get_exception_stack()
    # end def get_traceback_stack

    @staticmethod
    def get_exception_stack():
        exception_trace = "\n========== Exception stack - START ==========\n"
        exception_trace += format_exc()
        exception_trace += "\n=========== Exception stack - END ===========\n"
        return exception_trace
    # end def get_exception_stack

    @staticmethod
    def get_regular_stack():
        exception_trace = "\n========== Regular stack - START ==========\n"
        exception_trace += "".join(format_stack())
        exception_trace += "\n=========== Regular stack - END ===========\n"
        return exception_trace
    # end def get_regular_stack
# end class TracebackLogWrapper


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
