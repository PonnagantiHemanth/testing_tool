#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_1803.testrunner
:brief: HID++ 2.0 feature 0x1803 testrunner implementation
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/09/16
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1803.errorhandling import GpioAccessErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1803.functionality import GpioAccessFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1803.interface import GpioAccessInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1803.robustness import GpioAccessRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1803TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1803 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, GpioAccessInterfaceTestCase)
        self.runTest(result, context, GpioAccessFunctionalityTestCase)
        self.runTest(result, context, GpioAccessErrorHandlingTestCase)
        self.runTest(result, context, GpioAccessRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1803TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
