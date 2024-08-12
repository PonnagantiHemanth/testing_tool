#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4540.testrunner
:brief: HID++ 2.0 feature 0x4540 testrunner implementation
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4540.errorhandling import \
    KeyboardInternationalLayoutsErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4540.functionality import \
    KeyboardInternationalLayoutsFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4540.interface import KeyboardInternationalLayoutsInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4540.robustness import KeyboardInternationalLayoutsRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature4540TestSuite(PyHarnessSuite):
    """
    Define test runner suite for keyboard feature 0x4540 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, KeyboardInternationalLayoutsInterfaceTestCase)
        self.runTest(result, context, KeyboardInternationalLayoutsFunctionalityTestCase)
        self.runTest(result, context, KeyboardInternationalLayoutsErrorHandlingTestCase)
        self.runTest(result, context, KeyboardInternationalLayoutsRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4540TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
