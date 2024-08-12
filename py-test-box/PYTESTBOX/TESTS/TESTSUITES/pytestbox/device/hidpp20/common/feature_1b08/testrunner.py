#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1b08.testrunner
:brief: HID++ 2.0 feature 0x1b08 testrunner implementation
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_1b08.errorhandling import AnalogKeysErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_1b08.functionality import AnalogKeysFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_1b08.interface import AnalogKeysInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_1b08.robustness import AnalogKeysRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature1B08TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x1B08 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.

        :param result: The test result that will collect the results.
        :type result: ``TestResult``
        :param context: The context in which the tests are run.
        :type context: ``Context``
        """
        self.runTest(result, context, AnalogKeysInterfaceTestCase)
        self.runTest(result, context, AnalogKeysFunctionalityTestCase)
        self.runTest(result, context, AnalogKeysErrorHandlingTestCase)
        self.runTest(result, context, AnalogKeysRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature1B08TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
