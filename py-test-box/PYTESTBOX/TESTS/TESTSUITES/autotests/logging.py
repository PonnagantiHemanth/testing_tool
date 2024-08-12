#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package autotests.logging

@brief  Test example Logging facilities

@author christophe.roquebert

@date   2018/08/24
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from time                               import sleep

from pyharness.extensions                import PyHarnessCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class LoggingTestCase(PyHarnessCase):                                                                                    # pylint:disable=R0901
    """
    A TestCase that logs information.
    """
    TIME_SLEEP = 0.5

    def testLog(self):
        """
        Uses various logging functions
        """
        self.logTitle1("This is the first level 1 title")
        self.logTrace('New trace')
        self.logTrace('Another trace')
        sleep(self.TIME_SLEEP)

        self.logTitle2("Here is a level 2 title")
        self.logTrace('New trace')
        self.logTrace('Another trace')
        sleep(self.TIME_SLEEP)

        self.logTitle2("And another one")
        sleep(self.TIME_SLEEP)

        self.logTitle3("And finally a level 3 title")
        sleep(self.TIME_SLEEP)

        self.logTitle1("This is the second level 1 title")
        sleep(self.TIME_SLEEP)

        self.logTitle2("New level 2 title")
        sleep(self.TIME_SLEEP)

        self.logTitle3("New level 3 title")
        sleep(self.TIME_SLEEP)

        self.logTitle3("Another level 3 title")
        self.logTrace('New trace')
        self.logTrace('Another trace')
        sleep(self.TIME_SLEEP)

        self.logTitle2("Another level 2 title")
        sleep(self.TIME_SLEEP)

        self.logTitle3("New level 3 title")
        self.logTrace('New trace')
        self.logTrace('Another trace')
        sleep(self.TIME_SLEEP)

        self.logTitle3("Another level 3 title")
        self.logTrace('New trace')
        self.logTrace('Another trace')
        sleep(self.TIME_SLEEP)
    # end def testLog
# end class LoggingTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
