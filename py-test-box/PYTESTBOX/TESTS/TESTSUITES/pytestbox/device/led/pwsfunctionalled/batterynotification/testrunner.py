#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.led.pwsfunctionalled.batterynotification
:brief: battery notification testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.led.pwsfunctionalled.batterynotification.functionality import \
    BatteryNotificationBleFunctionalityTestCase
from pytestbox.device.led.pwsfunctionalled.batterynotification.functionality import \
    BatteryNotificationFunctionalityTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BatteryNotificationTestSuite(PyHarnessSuite):
    """
    Test runner class for battery notification test suite
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite
        """
        self.runTest(result, context, BatteryNotificationFunctionalityTestCase)
        self.runTest(result, context, BatteryNotificationBleFunctionalityTestCase)
    # end def runTests
# end class BatteryNotificationTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
