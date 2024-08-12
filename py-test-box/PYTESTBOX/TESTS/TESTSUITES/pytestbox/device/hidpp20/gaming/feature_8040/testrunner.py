#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.gaming.feature_8040.testrunner
:brief: HID++ 2.0 feature 0x8040 testrunner implementation
:author: YY Liu <yliu5@logitech.com>
:date: 2023/11/15
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.gaming.feature_8040.business import BrightnessControlBusinessTestCase
from pytestbox.device.hidpp20.gaming.feature_8040.errorhandling import BrightnessControlErrorHandlingTestCase
from pytestbox.device.hidpp20.gaming.feature_8040.functionality import BrightnessControlFunctionalityTestCase
from pytestbox.device.hidpp20.gaming.feature_8040.interface import BrightnessControlInterfaceTestCase
from pytestbox.device.hidpp20.gaming.feature_8040.robustness import BrightnessControlRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature8040TestSuite(PyHarnessSuite):
    """
    Define test runner suite for gaming feature 0x8040 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, BrightnessControlInterfaceTestCase)
        self.runTest(result, context, BrightnessControlBusinessTestCase)
        self.runTest(result, context, BrightnessControlFunctionalityTestCase)
        self.runTest(result, context, BrightnessControlErrorHandlingTestCase)
        self.runTest(result, context, BrightnessControlRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature8040TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
