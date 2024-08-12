#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.mouse.feature_2251.testrunner
:brief: HID++ 2.0 feature 0x2251 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2251.business import MouseWheelAnalyticsBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2251.errorhandling import MouseWheelAnalyticsErrorHandlingTestCase
from pytestbox.device.hidpp20.mouse.feature_2251.functionality import MouseWheelAnalyticsFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2251.interface import MouseWheelAnalyticsInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2251.robustness import MouseWheelAnalyticsRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature2251TestSuite(PyHarnessSuite):
    """
    Define test runner suite for mouse feature 0x2251 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, MouseWheelAnalyticsInterfaceTestCase)
        self.runTest(result, context, MouseWheelAnalyticsBusinessTestCase)
        self.runTest(result, context, MouseWheelAnalyticsFunctionalityTestCase)
        self.runTest(result, context, MouseWheelAnalyticsErrorHandlingTestCase)
        self.runTest(result, context, MouseWheelAnalyticsRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2251TestSuite
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
