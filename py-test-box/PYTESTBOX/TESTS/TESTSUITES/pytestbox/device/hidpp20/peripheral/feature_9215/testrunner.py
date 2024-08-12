#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.peripheral.feature_9215.testrunner
:brief: HID++ 2.0 feature 0x9215 testrunner implementation
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/06/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.peripheral.feature_9215.business import Ads1231BusinessTestCase
from pytestbox.device.hidpp20.peripheral.feature_9215.errorhandling import Ads1231ErrorHandlingTestCase
from pytestbox.device.hidpp20.peripheral.feature_9215.functionality import Ads1231FunctionalityTestCase
from pytestbox.device.hidpp20.peripheral.feature_9215.interface import Ads1231InterfaceTestCase
from pytestbox.device.hidpp20.peripheral.feature_9215.robustness import Ads1231RobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature9215TestSuite(PyHarnessSuite):
    """
    Define test runner suite for peripheral feature 0x9215 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, Ads1231InterfaceTestCase)
        self.runTest(result, context, Ads1231BusinessTestCase)
        self.runTest(result, context, Ads1231FunctionalityTestCase)
        self.runTest(result, context, Ads1231ErrorHandlingTestCase)
        self.runTest(result, context, Ads1231RobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature9215TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
