#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_180b.testrunner
:brief: HID++ 2.0 feature 0x180b testrunner implementation
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/04/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_180b.errorhandling import ConfigurableDeviceRegistersErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_180b.interface import ConfigurableDeviceRegistersInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_180b.functionality import ConfigurableDeviceRegistersFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_180b.robustness import ConfigurableDeviceRegistersRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature180BTestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x180B tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.

        :param result: The collector for the test results.
        :type result: ``TestResult``
        :param context: The context in which the tests will run
        :type context: ``Context``
        """
        self.runTest(result, context, ConfigurableDeviceRegistersInterfaceTestCase)
        self.runTest(result, context, ConfigurableDeviceRegistersFunctionalityTestCase)
        self.runTest(result, context, ConfigurableDeviceRegistersErrorHandlingTestCase)
        self.runTest(result, context, ConfigurableDeviceRegistersRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature180BTestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
