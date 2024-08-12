#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.mouse.feature_2150.testrunner
:brief: HID++ 2.0 feature 0x2150 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.mouse.feature_2150.business import ThumbwheelBusinessTestCase
from pytestbox.device.hidpp20.mouse.feature_2150.errorhandling import ThumbwheelErrorHandlingTestCase
from pytestbox.device.hidpp20.mouse.feature_2150.functionality import ThumbwheelFunctionalityTestCase
from pytestbox.device.hidpp20.mouse.feature_2150.interface import ThumbwheelInterfaceTestCase
from pytestbox.device.hidpp20.mouse.feature_2150.robustness import ThumbwheelRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature2150TestSuite(PyHarnessSuite):
    """
    Define test runner suite for mouse feature 0x2150 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, ThumbwheelInterfaceTestCase)
        self.runTest(result, context, ThumbwheelBusinessTestCase)
        self.runTest(result, context, ThumbwheelFunctionalityTestCase)
        self.runTest(result, context, ThumbwheelRobustnessTestCase)
        self.runTest(result, context, ThumbwheelErrorHandlingTestCase)
    # end def runTests
# end class DeviceHidpp20Feature2150TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
