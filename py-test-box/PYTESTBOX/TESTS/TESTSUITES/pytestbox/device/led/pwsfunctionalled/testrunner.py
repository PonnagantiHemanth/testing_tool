#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.led.pwsfunctionalled.testrunner
:brief: Pws functional leds testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.led.pwsfunctionalled.batterynotification.testrunner import BatteryNotificationTestSuite


# ----------------------------------------------------------------------------------------------------------------------
# importation
# ----------------------------------------------------------------------------------------------------------------------
class PWSFunctionalLedTestSuite(PyHarnessSuite):
    """
    Test runner class for pws functional led evt automation test suites
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, BatteryNotificationTestSuite)
    # end def runTests
# end class PWSFunctionalLedTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
