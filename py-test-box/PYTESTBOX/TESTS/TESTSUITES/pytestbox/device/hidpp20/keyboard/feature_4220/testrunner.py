#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.keyboard.feature_4220.testrunner
:brief: HID++ 2.0 feature 0x4220 testrunner implementation
:author: Anil Gadad <agadad@logitech.com>
:date: 2022/04/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4220.business import LockKeyStateBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_4220.errorhandling import LockKeyStateErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4220.functionality import LockKeyStateFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4220.interface import LockKeyStateInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4220.robustness import LockKeyStateRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature4220TestSuite(PyHarnessSuite):
    """
    Define test runner suite for keyboard feature 0x4220 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, LockKeyStateInterfaceTestCase)
        self.runTest(result, context, LockKeyStateBusinessTestCase)
        self.runTest(result, context, LockKeyStateFunctionalityTestCase)
        self.runTest(result, context, LockKeyStateErrorHandlingTestCase)
        self.runTest(result, context, LockKeyStateRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4220TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
