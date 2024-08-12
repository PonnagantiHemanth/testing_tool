#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.hidpp20.keyboard.feature_4531.testrunner
:brief: HID++ 2.0 feature 0x4531 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2022/10/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4531.business import MultiPlatformBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_4531.errorhandling import MultiPlatformErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4531.functionality import MultiPlatformFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4531.interface import MultiPlatformInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4531.robustness import MultiPlatformRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature4531TestSuite(PyHarnessSuite):
    """
    Define test runner suite for keyboard feature 0x4531 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, MultiPlatformInterfaceTestCase)
        self.runTest(result, context, MultiPlatformBusinessTestCase)
        self.runTest(result, context, MultiPlatformFunctionalityTestCase)
        self.runTest(result, context, MultiPlatformErrorHandlingTestCase)
        self.runTest(result, context, MultiPlatformRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4531TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
