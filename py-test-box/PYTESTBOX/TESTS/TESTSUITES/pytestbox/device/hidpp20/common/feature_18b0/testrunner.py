#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.common.feature_18b0.testrunner
:brief: HID++ 2.0 feature 0x18b0 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.common.feature_18b0.business import StaticMonitorModeBusinessTestCase
from pytestbox.device.hidpp20.common.feature_18b0.errorhandling import StaticMonitorModeErrorHandlingTestCase
from pytestbox.device.hidpp20.common.feature_18b0.functionality import StaticMonitorModeFunctionalityTestCase
from pytestbox.device.hidpp20.common.feature_18b0.interface import StaticMonitorModeInterfaceTestCase
from pytestbox.device.hidpp20.common.feature_18b0.performance import StaticMonitorModePerformanceTestCase
from pytestbox.device.hidpp20.common.feature_18b0.robustness import StaticMonitorModeRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature18B0TestSuite(PyHarnessSuite):
    """
    Define test runner suite for common feature 0x18B0 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, StaticMonitorModeInterfaceTestCase)
        self.runTest(result, context, StaticMonitorModeBusinessTestCase)
        self.runTest(result, context, StaticMonitorModeFunctionalityTestCase)
        self.runTest(result, context, StaticMonitorModeErrorHandlingTestCase)
        self.runTest(result, context, StaticMonitorModeRobustnessTestCase)
        self.runTest(result, context, StaticMonitorModePerformanceTestCase)
    # end def runTests
# end class DeviceHidpp20Feature18B0TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
