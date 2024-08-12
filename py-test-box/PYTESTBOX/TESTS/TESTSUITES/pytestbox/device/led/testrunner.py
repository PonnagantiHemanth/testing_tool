#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.led.testrunner
:brief: Pws functional leds testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.led.pwsfunctionalled.testrunner import PWSFunctionalLedTestSuite


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceLedTestSuite(PyHarnessSuite):
    """
    Test runner class for led evt automation test suite
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, PWSFunctionalLedTestSuite)
    # end def runTests
# end class DeviceLedTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
