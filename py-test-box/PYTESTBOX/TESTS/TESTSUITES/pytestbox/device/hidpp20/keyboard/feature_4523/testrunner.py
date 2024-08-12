#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.keyboard.feature_4523.testrunner
:brief: HID++ 2.0 feature 0x4523 testrunner implementation
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import PyHarnessSuite
from pytestbox.device.hidpp20.keyboard.feature_4523.business import DisableControlsByCIDXBusinessTestCase
from pytestbox.device.hidpp20.keyboard.feature_4523.errorhandling import DisableControlsByCIDXErrorHandlingTestCase
from pytestbox.device.hidpp20.keyboard.feature_4523.functionality import DisableControlsByCIDXFunctionalityTestCase
from pytestbox.device.hidpp20.keyboard.feature_4523.interface import DisableControlsByCIDXInterfaceTestCase
from pytestbox.device.hidpp20.keyboard.feature_4523.robustness import DisableControlsByCIDXRobustnessTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceHidpp20Feature4523TestSuite(PyHarnessSuite):
    """
    Define test runner suite for keyboard feature 0x4523 tests
    """

    def runTests(self, result, context):
        """
        Run all the tests in the test suite.
        """
        self.runTest(result, context, DisableControlsByCIDXInterfaceTestCase)
        self.runTest(result, context, DisableControlsByCIDXBusinessTestCase)
        self.runTest(result, context, DisableControlsByCIDXFunctionalityTestCase)
        self.runTest(result, context, DisableControlsByCIDXErrorHandlingTestCase)
        self.runTest(result, context, DisableControlsByCIDXRobustnessTestCase)
    # end def runTests
# end class DeviceHidpp20Feature4523TestSuite

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
